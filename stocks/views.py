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
            ticker = self.get_ticker_from_company_name(search_term)
            self.save_to_database(ticker, search_term)
            return redirect('stocks:intro', ticker=ticker)
        except Exception as e:
            messages.error(request, f"'{search_term}'에 해당하는 주식 티커를 찾을 수 없습니다. 다시 시도해주세요.")
            return self.get(request, *args, **kwargs)

    def get_ticker_from_company_name(self, company_name):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that converts company names to stock ticker symbols."},
                {"role": "user", 
                 "content": f"Convert {company_name} to a ticker so that I can search for stocks in the Python yfinance library. Please give me only the ticker as the answer."}
            ],
            max_tokens=60,
        )
        return response.choices[0].message['content'].strip()

    def save_to_database(self, ticker, search_term):
        stock_obj, created = Stock.objects.get_or_create(ticker=ticker, defaults={'company_name': search_term})
        StockSearch.objects.create(stock=stock_obj, search_term=search_term)

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