from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Symbol(models.Model):
    code = models.CharField(max_length=10)                            
    company_name = models.CharField(max_length=200)
    screener = models.CharField(max_length=200)
    exchange = models.CharField(max_length=200)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.code


class SymbolDailyInfo(models.Model):
    symbol = models.ForeignKey(Symbol, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    rsi = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    volume = models.DecimalField(default=0, max_digits=20, decimal_places=4)
    open = models.DecimalField(default=0, max_digits=20, decimal_places=4)
    close = models.DecimalField(default=0, max_digits=20, decimal_places=4)
    sma10 = models.DecimalField(default=0, max_digits=20, decimal_places=4)

    def __str__(self):
        return f"{self.symbol.code}_{self.date.strftime('%d/%m/%Y')}"