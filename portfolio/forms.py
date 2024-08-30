from django import forms
from django.forms import inlineformset_factory
from .models import Portfolio, PortfolioStock
from stocks.models import Stock

class PortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ['name']

class PortfolioStockForm(forms.ModelForm):
    ticker = forms.CharField(max_length=10, label="Ticker")

    class Meta:
        model = PortfolioStock
        fields = ['ticker', 'quantity', 'purchase_price']

    def clean_ticker(self):
        ticker = self.cleaned_data['ticker']
        if not Stock.objects.filter(ticker=ticker).exists():
            raise forms.ValidationError(f"Stock with ticker '{ticker}' does not exist.")
        return ticker

PortfolioStockFormSet = inlineformset_factory(
    Portfolio, PortfolioStock,
    form=PortfolioStockForm,
    extra=1,
    can_delete=True
)

