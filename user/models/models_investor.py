from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from user.models import Symbol


class Investor(models.Model):
    name = models.CharField(max_length=200)
    telegram_id = models.DecimalField(null=True, blank=True, max_digits=15, decimal_places=0)
    login_account = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    expired_date = models.DateTimeField(default=timezone.now)       
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def display_expired_date(self):
        return self.expired_date.strftime('%d/%m/%Y')

class StockAsset(models.Model):
    investor = models.ForeignKey(Investor, on_delete=models.CASCADE)
    symbol = models.ForeignKey(Symbol, on_delete=models.CASCADE)