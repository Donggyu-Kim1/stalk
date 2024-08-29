from django import forms
from .models import Portfolio, PortfolioStock

class PortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ['name']

class PortfolioStockForm(forms.ModelForm):
    class Meta:
        model = PortfolioStock
        fields = ['quantity', 'purchase_price']
