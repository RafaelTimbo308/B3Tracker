from django.utils import timezone
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from .models import Ticker
import yfinance as yf
from .tasks import create_monitoring_thread
# Create your views here.


def Home(request):

    if request.method =="POST":
    
        code = request.POST.get('ticker').upper()
        tunnel_inf = request.POST.get('tunnel-inf')
        tunnel_sup = request.POST.get('tunnel-sup')
        now = timezone.now()
        interval = request.POST.get('interval')
        try:
            value = yf.Ticker(code+".SA").history(period="1d")['Close'].iloc[-1]
        except:
            tickers = Ticker.objects.all()
            error_msg = f"Ação {code} não encontrada."
            return render(request , "Ticker/home.html",{
                "tickers":tickers,
                "error":error_msg,
            })

        new_obj = Ticker(
            ticker = code,
            tunnel_inf = tunnel_inf,
            tunnel_sup = tunnel_sup,
            value = value,
            interval = interval,
                last_update = now)

        if Ticker.objects.filter(ticker = code).exists() == False:
            new_obj.save()
            create_monitoring_thread(code)
        
        new_obj.save()
        
    tickers = Ticker.objects.all()
    
    return render(request , "Ticker/home.html", {
        "tickers":tickers
    })