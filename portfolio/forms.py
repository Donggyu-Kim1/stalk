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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['ticker'].initial = self.instance.stock.ticker
        
        # 삭제 예정인 폼의 경우 필드를 필수가 아니게 설정
        if 'data' in kwargs and kwargs['data'].get(f'{kwargs.get("prefix", "")}-DELETE'):
            for field in self.fields.values():
                field.required = False

PortfolioStockFormSet = inlineformset_factory(
    Portfolio, PortfolioStock,
    form=PortfolioStockForm,
    extra=5,
    can_delete=True,
    can_delete_extra=True,  # 추가된 빈 폼도 삭제 가능하게 함
    min_num=1,  # 최소 1개의 폼은 유지
    validate_min=True,  # 최소 폼 개수 검증
)