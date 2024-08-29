from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import Stock
import yfinance as yf
from googletrans import Translator


class StocksSearchView(ListView):
    model = Stock
    template_name = 'stocks/stocks_search.html'
    context_object_name = 'stocks'
    paginate_by = 20

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Stock.objects.filter(
                Q(ticker__icontains=query) | 
                Q(company_name__icontains=query)
            ).order_by('ticker')
        return Stock.objects.all().order_by('ticker')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context


class StockDetailView(DetailView):
    model = Stock
    template_name = 'stocks/stocks_detail.html'
    context_object_name = 'stock'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ticker = self.object.ticker

        # Yahoo Finance에서 주식 정보 가져오기
        stock = yf.Ticker(ticker)

        # 번역기 설정
        translator = Translator()
        target_language = 'ko'

        # 기업 소개 번역
        company_info = stock.info.get('longBusinessSummary', 'No information available')
        translated_company_info = translator.translate(company_info, dest=target_language).text
        context['company_info'] = translated_company_info

        # 뉴스
        context['news'] = stock.news

        # 차트 데이터
        hist = stock.history(period="1mo")
        context['chart_data'] = hist['Close'].to_json(date_format='iso')

        # 재무제표 번역
        financials = stock.financials
        if not financials.empty:
            # 계정과목 한국어 번역
            translated_financials = financials.rename(
                lambda x: translator.translate(x, dest=target_language).text, axis='index'
            )
            context['financials'] = translated_financials.to_html(classes='table table-striped')
        else:
            context['financials'] = "No financial data available"

        return context