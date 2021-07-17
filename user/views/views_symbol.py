from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.views.decorators.clickjacking import xframe_options_exempt
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings

from tradingview_ta import TA_Handler, Interval, Exchange
from telegram.ext import Updater
from telegram.ext import CommandHandler
from helpers.telegramHelper import TelegramHelper

from user.forms import CreateUserForm
from user.forms import LoginForm
from user.models import Investor, Symbol, StockAsset, SymbolDailyInfo


def run_telegram():
    updater = Updater(token=settings.TELEGRAM_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('stock', stock)
    dispatcher.add_handler(start_handler)
    updater.start_polling()


@login_required
def list_symbol_asset(request):
    if not settings.IS_RUN_TELEGRAM: 
        settings.IS_RUN_TELEGRAM = True
        run_telegram()

    stock_assets = Investor.objects.filter(login_account=request.user).first().stockasset_set.all()
    
    context = {
        'stock_assets': stock_assets,
        'symbols': Symbol.objects.filter(is_deleted=False)
    }    

    return render(request, "user/stock/list_symbol_asset.html", context)


def stock(update, context):
    for item in StockAsset.objects.all():

        data = TA_Handler(
            symbol=item.symbol.code,
            screener=item.symbol.screener,
            exchange=item.symbol.exchange,
            interval=Interval.INTERVAL_1_DAY
        )

        symbol_code = item.symbol.code
        rsi = data.get_analysis().indicators['RSI']
        volume = data.get_analysis().indicators['volume']
        open = data.get_analysis().indicators['open']
        close = data.get_analysis().indicators['close']
        sma10 = data.get_analysis().indicators['SMA10']

        symbol_daily_info = SymbolDailyInfo(
            symbol=item.symbol,
            rsi = rsi,
            volume = volume,
            open = open,
            close = close,
            sma10 = sma10
        )
        symbol_daily_info.save()

        telegram_message = f""" 
            Mã: {symbol_code},
            RSI: {rsi},
            VOLUME: {volume:,},
            OPEN: {open:,},
            CLOSE: {close:,},
            SMA10: {sma10:,},
        """

        context.bot.send_message(chat_id=update.effective_chat.id, text=telegram_message)

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


    