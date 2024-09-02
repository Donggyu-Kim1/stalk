from django.db import models
from django.contrib.auth.models import User
from stocks.models import Stock  # Stock 모델을 stocks 앱에서 가져오기

class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='portfolios')
    name = models.CharField(max_length=255)  # 포트폴리오 이름
    created_at = models.DateTimeField(auto_now_add=True)  # 생성일

    def __str__(self):
        return self.name

class PortfolioStock(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='stocks')
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)  # stocks 앱의 Stock 모델 참조
    quantity = models.PositiveIntegerField()  # 보유 주식 수량
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)  # 매수 가격
    created_at = models.DateTimeField(auto_now_add=True)  # 추가된 날짜

    def __str__(self):
        return f'{self.stock.ticker} in {self.portfolio.name}'

    class Meta:
        unique_together = ['portfolio', 'stock']  # 포트폴리오에 동일 주식을 중복 추가 X

