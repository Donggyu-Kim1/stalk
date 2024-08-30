from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Portfolio, PortfolioStock
from .forms import PortfolioForm, PortfolioStockFormSet
from stocks.models import Stock
import yfinance as yf
from decimal import Decimal

class PortfolioListView(LoginRequiredMixin, ListView):
    model = Portfolio
    template_name = 'portfolio/portfolio_list.html'
    context_object_name = 'portfolios'

    def get_queryset(self):
        return Portfolio.objects.filter(user=self.request.user)


class PortfolioCreateView(LoginRequiredMixin, CreateView):
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

        # Portfolio 객체를 먼저 저장
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()

        if formset.is_valid():
            # 모든 formset 인스턴스에서 PortfolioStock 객체를 생성하고 저장
            for stock_form in formset:
                portfolio_stock = stock_form.save(commit=False)
                portfolio_stock.portfolio = self.object  # 현재 포트폴리오와 연결
                # Stock 객체를 티커로 찾은 후 PortfolioStock 객체에 할당
                ticker = stock_form.cleaned_data.get('ticker')
                if ticker:
                    stock = Stock.objects.get(ticker=ticker)
                    portfolio_stock.stock = stock
                    portfolio_stock.save()  # PortfolioStock 객체 저장

            return super().form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('portfolio:portfolio_read', kwargs={'pk': self.object.pk})


class PortfolioReadView(LoginRequiredMixin, DetailView):
    model = Portfolio
    template_name = 'portfolio/portfolio_read.html'
    context_object_name = 'portfolio'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        portfolio_stocks = PortfolioStock.objects.filter(portfolio=self.object).select_related('stock')

        # 각 주식의 마지막 종가를 가져와 수익률을 계산
        stocks = []
        total_value = 0
        for portfolio_stock in portfolio_stocks:
            ticker = portfolio_stock.stock.ticker
            purchase_price = portfolio_stock.purchase_price
            quantity = portfolio_stock.quantity
            current_price = yf.Ticker(ticker).history(period='1d')['Close'].iloc[0]
            value = current_price * quantity
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

        context['stocks'] = stocks
        return context


class PortfolioDeleteView(LoginRequiredMixin, DeleteView):
    model = Portfolio
    template_name = 'portfolio/portfolio_delete.html'
    success_url = reverse_lazy('portfolio:portfolio_list')
