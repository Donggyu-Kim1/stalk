from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from .models import Portfolio, PortfolioStock
from .forms import PortfolioForm, PortfolioStockForm, PortfolioStockFormSet
from stocks.models import Stock


class PortfolioListView(LoginRequiredMixin, ListView):
    model = Portfolio
    template_name = 'portfolio/portfolio_list.html'
    context_object_name = 'portfolios'

    def get_queryset(self):
        return Portfolio.objects.filter(user=self.request.user)


class PortfolioCreateView(CreateView):
    model = Portfolio
    form_class = PortfolioForm
    template_name = 'portfolio/portfolio_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = PortfolioStockFormSet(self.request.POST)
        else:
            context['formset'] = PortfolioStockFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']

        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()  # 먼저 포트폴리오를 저장합니다.

        if formset.is_valid():
            formset.instance = self.object  # formset이 현재 저장된 Portfolio와 연결되도록 설정
            formset.save()  # formset을 저장하여 PortfolioStock 인스턴스를 생성합니다.
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('portfolio:portfolio_read', kwargs={'pk': self.object.pk})


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
