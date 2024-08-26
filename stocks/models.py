from django.db import models

class Stock(models.Model):
    stock_id = models.AutoField(primary_key=True)
    stock_symbol = models.CharField(max_length=20, unique=True)
    company_name = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.company_name} ({self.stock_symbol})"