from django import forms
from django.forms import inlineformset_factory  # form 편집 기능
from .models import Portfolio, PortfolioStock
from stocks.models import Stock

class PortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'autocomplete': 'name', # 자동완성 기능
            }),
        }

class PortfolioStockForm(forms.ModelForm):
    ticker = forms.CharField(
        max_length=10, 
        label="Ticker",
        widget=forms.TextInput(attrs={
            'autocomplete': 'ticker'
        }),
        required=True   # 각 항목들 필수로
    )
    
    quantity = forms.IntegerField(
        label="Quantity",
        widget=forms.NumberInput(attrs={
            'autocomplete': 'quantity'
        }),
        required=True
    )
    
    purchase_price = forms.DecimalField(
        label="Purchase price",
        widget=forms.NumberInput(attrs={
            'autocomplete': 'purchase_price'
        }),
        required=True
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
    
    # stock 테이블에 있는 ticker와 form에 입력한 ticker가 일치하지 않는다면 에러
    def clean_ticker(self):
        ticker = self.cleaned_data.get('ticker')
        if not Stock.objects.filter(ticker=ticker).exists():
            raise forms.ValidationError(f"Ticker '{ticker}'는 유효하지 않습니다. 존재하지 않는 티커입니다.")
        return ticker

PortfolioStockFormSet = inlineformset_factory(
    Portfolio, PortfolioStock,
    form=PortfolioStockForm,
    extra=5,    # 기본 5개
    can_delete=False, # html에서 delete 버튼을 이용해 삭제
)