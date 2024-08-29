from django import forms
from .models import Portfolio, PortfolioStock
import yfinance as yf

class PortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ['name']

class PortfolioStockForm(forms.ModelForm):
    class Meta:
        model = PortfolioStock
        fields = ['stock', 'quantity', 'purchase_price']

    def clean(self):
        cleaned_data = super().clean()
        ticker = cleaned_data.get("stock").ticker

        # yfinance로 티커가 유효한지 확인
        yf_stock = yf.Ticker(ticker)
        if yf_stock.history(period="1d").empty:
            raise forms.ValidationError(f"{ticker}은(는) 유효한 주식 티커가 아닙니다.")

        return cleaned_data
