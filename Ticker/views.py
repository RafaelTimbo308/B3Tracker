import yfinance as yf
from .models import Ticker
from .tasks import create_monitoring_thread
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.shortcuts import render, redirect
# Create your views here.

@login_required(login_url='login/')
def Home(request):

    if request.method =='GET':
        tickers = Ticker.objects.filter(user = request.user)
        name = request.user.first_name
        return render(request , "Ticker/home.html", {
            "tickers":tickers,
            "name":name
        })
    
    elif request.method =="POST":
        
        user = request.user
        code = request.POST.get('ticker').upper()
        tunnel_inf = request.POST.get('tunnel-inf')
        tunnel_sup = request.POST.get('tunnel-sup')
        now = timezone.now()
        interval = request.POST.get('interval')
        try:
            value = yf.Ticker(code+".SA").history(period="1d")['Close'].iloc[-1]
        except:
            tickers = Ticker.objects.filter(user = request.user)
            error_msg = f"Ativo {code} não encontrada."
            return render(request , "Ticker/home.html",{
                "tickers":tickers,
                "error":error_msg,
                "name":user.first_name
            })

        if Ticker.objects.filter(user = request.user, ticker = code).exists() == True:
            ticker = Ticker.objects.get(user = request.user , ticker = code)           
            ticker.tunnel_inf = tunnel_inf
            ticker.tunnel_sup = tunnel_sup
            ticker.interval = interval
            ticker.value = value
            ticker.last_update = now
            ticker.save()

        else:
            new_obj = Ticker(
                user = user,
                ticker = code,
                tunnel_inf = tunnel_inf,
                tunnel_sup = tunnel_sup,
                value = value,
                interval = interval,
                last_update = now)            
            new_obj.save()
            create_monitoring_thread(request.user , code)

    name = request.user.first_name
    tickers = Ticker.objects.filter(user = request.user)
    
    return render(request , "Ticker/home.html", {
        "tickers":tickers,
        "name":name
    })
        

@login_required(login_url='../login/')
def Detail(request):
    
    tickers = Ticker.objects.filter(user = request.user)
    
    tickers_formatted = []
    for ticker in tickers:
        ticker_formatted = {
            'last_update': ticker.get_last_update_formatted(),
            'ticker': ticker.ticker,
            'tunnel_inf': ticker.tunnel_inf,
            'tunnel_sup': ticker.tunnel_sup,
            'value': ticker.value,
            'interval': ticker.interval,
            # Adicione outros campos do objeto ticker conforme necessário
        }
        tickers_formatted.append(ticker_formatted)

    name = request.user.first_name
    return render(request, "Ticker/details.html", {
        "tickers": tickers_formatted,
        "name": name
    })

@login_required(login_url='../../login/')
def Delete(request,code):
    
    Ticker.objects.get(user = request.user, ticker=code).delete()
    
    return redirect('home')
    
def Cadaster(request):
    if request.method == "GET":
        return render(request , 'Ticker/cadaster.html')
    else:
        user_name = request.POST.get('name')
        user_surname = request.POST.get('surname')
        user_username = request.POST.get('username')
        user_mail=request.POST.get('email')
        user_password=request.POST.get('password')
        
        pre_username = User.objects.filter(username = user_username).first()
        pre_email = User.objects.filter(email = user_mail).first()
        
        if pre_username:
            error_msg='Nome de Usuário já cadastrado, tente outro.'
            return render(request,'Ticker/cadaster.html',{
                "error":error_msg
            })
        
        if pre_email:
            error_msg='E-mail já cadastrado.'
            return render(request,'Ticker/cadaster.html',{
                "error":error_msg
            })

        user = User.objects.create_user(
            first_name = user_name,
            last_name = user_surname,
            username=user_username,
            email=user_mail,
            password=user_password
        )
        user.save()
        
        return redirect('login')
        
        
        
def Login(request):
    if request.method == "GET":
        return render(request , 'Ticker/login.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username , password=password)
        
        if user:
            login(request, user)
            return redirect('home')
        
        else:    
            error_msg='Senha ou Nome de Usuário incorretos.'
            return render(request,'Ticker/login.html',{
                "error":error_msg
            })

def Logout(request):

    logout(request)
    return redirect('login')