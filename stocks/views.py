from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Stock, StockSearch
import openai
import yfinance as yf
import os

openai.api_key = os.getenv('OPEN_API_KEY')

class StocksSearchView(TemplateView):
    template_name = 'stocks/stocks_search.html'

    def post(self, request, *args, **kwargs):
        search_term = request.POST.get('search_term')
        
        try:
            # Use ChatGPT to convert company name to ticker
            response = openai.Completion.create(
              engine="text-davinci-002",
              prompt=f"Convert the company name '{search_term}' to its stock ticker symbol.",
              max_tokens=60
            )
            ticker = response.choices[0].text.strip()

            # Verify the ticker exists
            stock = yf.Ticker(ticker)
            if not stock.info.get('symbol'):
                raise ValueError("Invalid ticker")

            # Save to database
            stock_obj, created = Stock.objects.get_or_create(ticker=ticker, defaults={'company_name': search_term})
            StockSearch.objects.create(stock=stock_obj, search_term=search_term)

            return redirect('stocks_intro', ticker=ticker)
        except Exception as e:
            messages.error(request, f"'{search_term}'에 해당하는 주식 티커를 찾을 수 없습니다. 다시 시도해주세요.")
            return self.get(request, *args, **kwargs)

class StocksIntroView(TemplateView):
    template_name = 'stocks/stocks_intro.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ticker = self.kwargs.get('ticker')
        stock = yf.Ticker(ticker)
        context['stock_info'] = stock.info
        return context

class StocksNewsView(TemplateView):
    template_name = 'stocks/stocks_news.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ticker = self.kwargs.get('ticker')
        stock = yf.Ticker(ticker)
        context['news'] = stock.news
        return context

class StocksChartView(TemplateView):
    template_name = 'stocks/stocks_chart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ticker = self.kwargs.get('ticker')
        stock = yf.Ticker(ticker)
        context['history'] = stock.history(period="1y")
        return context

class StocksFinancialsView(TemplateView):
    template_name = 'stocks/stocks_financials.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ticker = self.kwargs.get('ticker')
        stock = yf.Ticker(ticker)
        context['financials'] = stock.financials
        context['balance_sheet'] = stock.balance_sheet
        context['cash_flow'] = stock.cashflow
        return context