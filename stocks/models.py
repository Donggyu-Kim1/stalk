from django.db import models

class Stock(models.Model):
    ticker = models.CharField(max_length=10, unique=True)
    company_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.company_name} ({self.ticker})"

class StockSearch(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name='searches')
    search_term = models.CharField(max_length=100)
    searched_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.search_term} -> {self.stock.ticker}"