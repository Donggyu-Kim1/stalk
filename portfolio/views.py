from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Portfolio, PortfolioStock
from .forms import PortfolioForm, PortfolioStockForm
from stocks.models import Stock
from django.http import JsonResponse


class PortfolioListView(LoginRequiredMixin, ListView):
    model = Portfolio
    template_name = 'portfolio/portfolio_list.html'
    context_object_name = 'portfolios'

    def get_queryset(self):
        return Portfolio.objects.filter(user=self.request.user)


class PortfolioSearchView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('query', '')
        if query:
            stocks = Stock.objects.filter(ticker__icontains=query) | Stock.objects.filter(company_name__icontains=query)
            results = [{'ticker': stock.ticker, 'company_name': stock.company_name} for stock in stocks]
            return JsonResponse({'results': results})
        return JsonResponse({'results': []})


class PortfolioCreateView(LoginRequiredMixin, CreateView):
    model = Portfolio
    form_class = PortfolioForm
    template_name = 'portfolio/portfolio_create.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        portfolio = form.save()

        # 세션에 저장된 주식을 포트폴리오에 추가
        for stock_data in self.request.session.get('selected_stocks', []):
            stock_instance = Stock.objects.get(ticker=stock_data['ticker'])
            quantity = int(stock_data['quantity'])
            purchase_price = float(stock_data['purchase_price'])

            PortfolioStock.objects.create(
                portfolio=portfolio,
                stock=stock_instance,
                quantity=quantity,
                purchase_price=purchase_price
            )

        # 세션에서 주식 데이터 제거
        self.request.session.pop('selected_stocks', None)

        return redirect(reverse_lazy('portfolio:portfolio_read', kwargs={'pk': portfolio.pk}))


class AddStockToPortfolioView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        ticker = request.POST.get('ticker')
        quantity = request.POST.get('quantity')
        purchase_price = request.POST.get('purchase_price')

        selected_stocks = request.session.get('selected_stocks', [])
        selected_stocks.append({
            'ticker': ticker,
            'quantity': quantity,
            'purchase_price': purchase_price,
        })
        request.session['selected_stocks'] = selected_stocks

        return JsonResponse({'message': '주식이 포트폴리오에 추가되었습니다.'})


class PortfolioReadView(LoginRequiredMixin, DetailView):
    model = Portfolio
    template_name = 'portfolio/portfolio_read.html'
    context_object_name = 'portfolio'


class PortfolioUpdateView(LoginRequiredMixin, UpdateView):
    model = PortfolioStock
    form_class = PortfolioStockForm
    template_name = 'portfolio/portfolio_update.html'

    def get_success_url(self):
        return reverse_lazy('portfolio:portfolio_read', kwargs={'pk': self.object.portfolio.pk})


class PortfolioDeleteView(LoginRequiredMixin, DeleteView):
    model = Portfolio
    template_name = 'portfolio/portfolio_delete.html'
    success_url = reverse_lazy('portfolio:portfolio_list')
