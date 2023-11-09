from django.utils import timezone
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from .models import Ticker
import yfinance as yf
# Create your views here.


def Home(request):

    if request.method =="POST":
    
        ticker = request.POST.get('ticker')+".SA"
        tunnel_inf = request.POST.get('tunnel-inf')
        tunnel_sup = request.POST.get('tunnel-sup')
        now = timezone.now()
        value = yf.Ticker(ticker).history(period="1d")['Close'].iloc[-1]
        interval = request.POST.get('interval')
        
        new_obj = Ticker(
            ticker = ticker,
            tunnel_inf = tunnel_inf,
            tunnel_sup = tunnel_sup,
            value = value,
            interval = interval,
            last_update = now
        )
        
        new_obj.save()
            
    tickers = Ticker.objects.all()
    
    return render(request , "Ticker/home.html", {
        "tickers":tickers
    })