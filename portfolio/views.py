from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Portfolio, PortfolioStock
from .forms import PortfolioForm, PortfolioStockFormSet
from stocks.models import Stock
import yfinance as yf
from decimal import Decimal

class PortfolioListView(LoginRequiredMixin, ListView):
    '''
    포트폴리오 모델 사용
    템플릿에서 portfolios로 리스트 값 사용
    포트폴리오 모델에서 user 값에 담긴 쿼리를 불러와 리스트에 담음
    '''
    model = Portfolio
    template_name = 'portfolio/portfolio_list.html'
    context_object_name = 'portfolios'

    def get_queryset(self):
        return Portfolio.objects.filter(user=self.request.user)


class PortfolioCreateView(LoginRequiredMixin, CreateView):
    '''
    포트폴리오 만들기 기능
    Post 요청(제출)의 경우, post 데이터를 사용하여 폼셋 초기화
    prefix를 통해 다른 폼과 구별
    get 요청(페이지 로드)의 겅우, 빈 폼셋 초기화
    폼 유효성 검사, 폼셋이 모두 유효한 경우에만 db에 저장
    '''
    model = Portfolio
    form_class = PortfolioForm
    template_name = 'portfolio/portfolio_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = PortfolioStockFormSet(self.request.POST, prefix='stock')
        else:
            context['formset'] = PortfolioStockFormSet(prefix='stock')
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']

        if form.is_valid() and formset.is_valid():
            self.object = form.save(commit=False)
            self.object.user = self.request.user
            self.object.save()

            for stock_form in formset:
                if stock_form.cleaned_data:
                    portfolio_stock = stock_form.save(commit=False)
                    portfolio_stock.portfolio = self.object

                    ticker = stock_form.cleaned_data.get('ticker')
                    if ticker:
                        stock = Stock.objects.get(ticker=ticker)
                        portfolio_stock.stock = stock
                        portfolio_stock.save()

            return super().form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('portfolio:portfolio_read', kwargs={'pk': self.object.pk})


class PortfolioReadView(LoginRequiredMixin, DetailView):
    '''
    포트폴리오 수익률 계산
    select_related로 stock 값도 미리 가져옴, 데이터베이스 쿼리 회수 감소
    '''
    model = Portfolio
    template_name = 'portfolio/portfolio_read.html'
    context_object_name = 'portfolio'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        portfolio_stocks = PortfolioStock.objects.filter(portfolio=self.object).select_related('stock')

        # 각 주식의 마지막 종가를 가져와 수익률을 계산
        stocks = []
        total_purchase_price = 0
        total_value = 0
        for portfolio_stock in portfolio_stocks:
            ticker = portfolio_stock.stock.ticker
            purchase_price = portfolio_stock.purchase_price
            quantity = portfolio_stock.quantity
            current_price = yf.Ticker(ticker).history(period='1d')['Close'].iloc[0]
            value = current_price * quantity
            total_purchase_price += purchase_price * quantity
            total_value += value
            stock = {
                'ticker': ticker,
                'purchase_price': purchase_price,
                'quantity': quantity,
                'current_price': current_price,
                'value': value,
                'return_rate': round((Decimal(current_price) - purchase_price) / purchase_price * 100, 2),
            }
            stocks.append(stock)

        # 전체 포트폴리오 수익률을 계산
        portfolio_return_rate = round((Decimal(total_value) - total_purchase_price) / total_purchase_price * 100, 2)

        context['stocks'] = stocks
        context['portfolio_return_rate'] = portfolio_return_rate
        return context


class PortfolioDeleteView(LoginRequiredMixin, DeleteView):
    '''
    포트폴리오 삭제 기능
    '''
    model = Portfolio
    template_name = 'portfolio/portfolio_delete.html'
    success_url = reverse_lazy('portfolio:portfolio_list')
