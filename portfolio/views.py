from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Portfolio, PortfolioStock
from .forms import PortfolioForm, PortfolioStockFormSet
from stocks.models import Stock


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
        context['portfolio_stocks'] = PortfolioStock.objects.filter(portfolio=self.object).select_related('stock')
        return context


class PortfolioDeleteView(LoginRequiredMixin, DeleteView):
    model = Portfolio
    template_name = 'portfolio/portfolio_delete.html'
    success_url = reverse_lazy('portfolio:portfolio_list')
