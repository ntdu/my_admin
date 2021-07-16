from django.core.management.base import BaseCommand, CommandError
from tradingview_ta import TA_Handler, Interval, Exchange

from user.models import Investor, Symbol, StockAsset, SymbolDailyInfo


class Command(BaseCommand):
    help = 'Lay thong tin Symbol'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        for item in StockAsset.objects.all():

            data = TA_Handler(
                symbol=item.symbol.code,
                screener=item.symbol.screener,
                exchange=item.symbol.exchange,
                interval=Interval.INTERVAL_1_DAY
            )
            
            symbol_daily_info = SymbolDailyInfo(
                symbol=item.symbol,
                rsi = data.get_analysis().indicators['RSI'],
                volume = data.get_analysis().indicators['volume'],
                open = data.get_analysis().indicators['open'],
                close = data.get_analysis().indicators['close'],
                sma10 = data.get_analysis().indicators['SMA10']
            )
            symbol_daily_info.save()
            
        self.stdout.write(self.style.SUCCESS('Successfull!!!'))