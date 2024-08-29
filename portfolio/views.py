from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .models import Portfolio, PortfolioStock, Stock
from .forms import PortfolioForm, PortfolioStockForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
import yfinance as yf

# 포트폴리오 리스트 보기
class PortfolioListView(LoginRequiredMixin, ListView):
    model = Portfolio
    context_object_name = 'portfolios'
    template_name = 'portfolio_list.html'

    def get_queryset(self):
        return Portfolio.objects.filter(user=self.request.user)

# 포트폴리오 생성
class PortfolioCreateView(LoginRequiredMixin, CreateView):
    model = Portfolio
    form_class = PortfolioForm
    template_name = 'portfolio_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        portfolio = form.save()

        # 포트폴리오에 최대 10개의 주식을 추가하는 로직
        for i in range(1, 11):  # 최대 10종목 추가
            stock_field = f'stock_{i}'
            quantity_field = f'quantity_{i}'
            purchase_price_field = f'purchase_price_{i}'

            stock = self.request.POST.get(stock_field)
            quantity = self.request.POST.get(quantity_field)
            purchase_price = self.request.POST.get(purchase_price_field)

            if stock and quantity and purchase_price:
                stock_instance, _ = Stock.objects.get_or_create(ticker=stock)
                PortfolioStock.objects.create(
                    portfolio=portfolio,
                    stock=stock_instance,
                    quantity=quantity,
                    purchase_price=purchase_price
                )

        # 생성된 포트폴리오의 상세 페이지로 리디렉션
        return redirect(reverse('portfolio_read', kwargs={'pk': portfolio.pk}))

# 포트폴리오 세부 보기 (그래프 생성)
class PortfolioReadView(LoginRequiredMixin, DetailView):
    model = Portfolio
    template_name = 'portfolio_detail.html'
    context_object_name = 'portfolio'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        portfolio = self.get_object()
        stocks = portfolio.stocks.all()

        # yfinance를 사용하여 주식 데이터 가져오기
        total_invested = 0
        total_current_value = 0
        sector_distribution = {}

        for stock_entry in stocks:
            ticker = stock_entry.stock.ticker
            yf_stock = yf.Ticker(ticker)
            current_price = yf_stock.history(period="1d")['Close'][0]

            # 총 투자금액 및 현재 가치 계산
            invested_amount = stock_entry.purchase_price * stock_entry.quantity
            current_value = current_price * stock_entry.quantity

            total_invested += invested_amount
            total_current_value += current_value

            # 산업 섹터 비율 계산 (가정: 섹터 정보가 주식 데이터에 포함됨)
            sector = yf_stock.info.get('sector', 'Unknown')
            sector_distribution[sector] = sector_distribution.get(sector, 0) + current_value

        # 수익률 계산
        context['profit_rate'] = (total_current_value - total_invested) / total_invested * 100 if total_invested > 0 else 0

        context['sector_distribution'] = sector_distribution
        return context

# 포트폴리오 업데이트
class PortfolioUpdateView(LoginRequiredMixin, UpdateView):
    model = Portfolio
    form_class = PortfolioForm
    template_name = 'portfolio_form.html'
    success_url = reverse_lazy('portfolio_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

# 포트폴리오 삭제
class PortfolioDeleteView(LoginRequiredMixin, DeleteView):
    model = Portfolio
    template_name = 'portfolio_confirm_delete.html'
    success_url = reverse_lazy('portfolio_list')
