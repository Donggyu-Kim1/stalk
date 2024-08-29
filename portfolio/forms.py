from django import forms
from .models import Portfolio, PortfolioStock

class PortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ['name']

class PortfolioStockForm(forms.ModelForm):
    class Meta:
        model = PortfolioStock
        fields = ['stock', 'quantity', 'purchase_price']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['quantity'].widget.attrs.update({'min': '1'})  # 최소 수량 1
        self.fields['purchase_price'].widget.attrs.update({'min': '0.01'})  # 최소 가격 0.01
