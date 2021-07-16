from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.views.decorators.clickjacking import xframe_options_exempt
from django.contrib.auth.decorators import login_required, permission_required

from tradingview_ta import TA_Handler, Interval, Exchange

from user.forms import CreateUserForm
from user.forms import LoginForm
from user.models import Investor, Symbol, StockAsset, SymbolDailyInfo


@login_required
def list_symbol_asset(request):
    stock_assets = Investor.objects.filter(login_account=request.user).first().stockasset_set.all()
    
    context = {
        'stock_assets': stock_assets,
        'symbols': Symbol.objects.filter(is_deleted=False)
    }    

    return render(request, "user/stock/list_symbol_asset.html", context)


@login_required
def create_symbol_asset(request):
    if request.method == 'POST':
        symbol_id = request.POST.get('symbol_id')

        stock_asset = StockAsset(
            investor = Investor.objects.filter(login_account=request.user).first(),
            symbol = Symbol.objects.filter(id=symbol_id).first()
        )
        stock_asset.save()

        return JsonResponse({'is_success': True})


@login_required
def delete_symbol_asset(request):
    if request.method == 'POST':
        symbol_id = request.POST.get('symbol_id')

        stock_asset = StockAsset.objects.filter(
            investor = Investor.objects.filter(login_account=request.user).first(),
            symbol = Symbol.objects.filter(id=symbol_id).first()
        )
        stock_asset.delete()

        return JsonResponse({'is_success': True})


def crawl_symbol_info(request):
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


    