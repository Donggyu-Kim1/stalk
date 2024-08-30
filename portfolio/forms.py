from django import forms
from django.forms import inlineformset_factory
from .models import Portfolio, PortfolioStock
from stocks.models import Stock

class PortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'autocomplete': 'name',
            }),
        }

class PortfolioStockForm(forms.ModelForm):
    ticker = forms.CharField(
        max_length=10, 
        label="Ticker",
        widget=forms.TextInput(attrs={
            'autocomplete': 'ticker'
        })
    )

    class Meta:
        model = PortfolioStock
        fields = ['ticker', 'quantity', 'purchase_price']
        widgets = {
            'quantity': forms.NumberInput(attrs={
                'autocomplete': 'quantity'
            }),
            'purchase_price': forms.NumberInput(attrs={
                'autocomplete': 'purchase_price'
            }),
        }

PortfolioStockFormSet = inlineformset_factory(
    Portfolio, PortfolioStock,
    form=PortfolioStockForm,
    extra=5,
    can_delete=True
)