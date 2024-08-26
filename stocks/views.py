import openai
from django.conf import settings
from django.views import View
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
import yfinance as yf
from .models import Stock

openai.api_key = settings.OPENAI_API_KEY

class stocksSearchView(View):
    def get(self, request):
        query = request.GET.get('query', '')
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that provides stock symbols for company names. Respond with only the stock symbol."},
                {"role": "user", "content": f"What is the stock symbol for {query}?"}
            ]
        )
        
        symbol = response.choices[0].message['content'].strip()
        
        try:
            stock = yf.Ticker(symbol)
            info = stock.info
            
            # Save or update stock information in the database
            stock_obj, created = Stock.objects.update_or_create(
                stock_symbol=symbol,
                defaults={'company_name': info.get('longName', query)}
            )
            
            data = {
                'stock_id': stock_obj.stock_id,
                'symbol': symbol,
                'name': stock_obj.company_name,
                'current_price': info.get('currentPrice', 'N/A'),
                'currency': info.get('currency', 'N/A'),
            }
            
            return JsonResponse(data)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

class stocksIntroView(View):
    def get(self, request, symbol):
        stock = get_object_or_404(Stock, stock_symbol=symbol)
        ticker = yf.Ticker(symbol)
        info = ticker.info
        
        data = {
            'stock_id': stock.stock_id,
            'symbol': stock.stock_symbol,
            'name': stock.company_name,
            'sector': info.get('sector', 'N/A'),
            'description': info.get('longBusinessSummary', 'No description available.'),
            'website': info.get('website', 'N/A'),
            'market_cap': info.get('marketCap', 'N/A'),
        }
        
        return render(request, 'stocks/intro.html', data)

class stocksNewsView(View):
    def get(self, request, symbol):
        stock = get_object_or_404(Stock, stock_symbol=symbol)
        ticker = yf.Ticker(symbol)
        news = ticker.news
        
        return render(request, 'stocks/news.html', {'stock': stock, 'news': news})

class stocksChartView(View):
    def get(self, request, symbol):
        stock = get_object_or_404(Stock, stock_symbol=symbol)
        ticker = yf.Ticker(symbol)
        history = ticker.history(period="1mo")
        
        chart_data = [
            {'date': date.strftime('%Y-%m-%d'), 'price': price} 
            for date, price in zip(history.index, history['Close'])
        ]
        
        return render(request, 'stocks/chart.html', {'stock': stock, 'chart_data': chart_data})

class stocksFinancialsView(View):
    def get(self, request, symbol):
        stock = get_object_or_404(Stock, stock_symbol=symbol)
        ticker = yf.Ticker(symbol)
        financials = ticker.financials
        
        return render(request, 'stocks/financials.html', {'stock': stock, 'financials': financials.to_dict()})

