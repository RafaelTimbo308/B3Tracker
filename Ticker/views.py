from django.utils import timezone
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from .models import Ticker
import yfinance as yf
# Create your views here.


def Home(request):

    if request.method =="POST":
    
        ticker = request.POST.get('ticker').upper()+".SA"
        tunnel_inf = request.POST.get('tunnel-inf')
        tunnel_sup = request.POST.get('tunnel-sup')
        now = timezone.now()
        interval = request.POST.get('interval')
        try:
            value = yf.Ticker(ticker).history(period="1d")['Close'].iloc[-1]
            new_obj = Ticker(
                ticker = ticker,
                tunnel_inf = tunnel_inf,
                tunnel_sup = tunnel_sup,
                value = value,
                interval = interval,
                last_update = now)  
            new_obj.save()            
        
        except:
            tickers = Ticker.objects.all()
            error_msg = f"Ação {ticker} não encontrada."
            return render(request , "Ticker/home.html",{
                "tickers":tickers,
                "error":error_msg,
            })
        
    tickers = Ticker.objects.all()
    
    return render(request , "Ticker/home.html", {
        "tickers":tickers
    })