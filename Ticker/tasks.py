from django.utils import timezone
from django.core.mail import send_mail
from .models import Ticker
import threading
import yfinance as yf

def send_mail_sell(ticker ,  value):
    
    send_mail(
        "Sugestão de Venda de Ativo",
        f'''
            Prezado usuário,
        
            O preço da ação {ticker} atingiu R${value}, ultrapassando o valor estipulado para venda.

            Atenciosamente,
            Equipe B3Tracker
        ''',
        "ticker.monitor2023@gmail.com",
        ["rafaelctimbo@gmail.com"],
        fail_silently=False,

    )

def send_mail_buy(ticker ,  value):
    
    send_mail(
        "Sugestão de Compra de Ativo",
        f'''
            Prezado usuário,
        
            O preço da ação {ticker} atingiu R${value}, ficando abaixo do valor estipulado para compra.

            Atenciosamente,
            Equipe B3Tracker
        ''',
        "ticker.monitor2023@gmail.com",
        ["rafaelctimbo@gmail.com"],
        fail_silently=False,

    )

def send_mail_upload(code):
    
    send_mail(
        f"Ativo {code} Adicionado ao Monitoramento!",
        f'''
            Prezado usuário,

            {code} foi inserido com sucesso aos ativos a serem monitorados!
            
            Atenciosamente,
            Equipe B3Tracker
        ''',
        "ticker.monitor2023@gmail.com",
        ["rafaelctimbo@gmail.com"],
        fail_silently=False,

    )

def monitoring(code):
    
    ticker = Ticker.objects.get(ticker = code+".SA")
    
    while True:
        
        last_update = ticker.last_update
        clock = timezone.now()
        delta = clock - last_update
        minutes = delta.seconds//60
        
        if minutes >= ticker.interval:
            value = yf.Ticker(code+".SA").history(period="1d")['Close'].iloc[-1]
            ticker.value = value
            ticker.last_update = timezone.now()
            ticker.save()
            
            if value > ticker.tunnel_sup:
                send_mail_sell(code , round(value,2))
            if value < ticker.tunnel_inf:
                send_mail_buy(code , round(value,2))

def create_monitoring_thread(code):
    send_mail_upload(code)
    monitoring_thread = threading.Thread(target=monitoring , args=(code,))
    monitoring_thread.start()