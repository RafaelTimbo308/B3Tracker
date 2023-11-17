from django.utils import timezone
from django.core.mail import send_mail
from .models import Ticker
import threading
import yfinance as yf
from time import sleep

def send_mail_sell(user , code ,  value):
    
    send_mail(
        f"Sugestão de Venda - {code}",
        f'''
            Prezado(a) {user.first_name} {user.last_name},
        
            O preço da ação {code} atingiu R${value}, ultrapassando o valor estipulado para venda.

            Atenciosamente,
            Equipe B3Tracker
        ''',
        "b3tracker@gmail.com",
        [f"{user.email}"],
        fail_silently=False,

    )

def send_mail_buy(user, code ,  value):
    
    send_mail(
        f"Sugestão de Compra - {code}",
        f'''
            Prezado(a) {user.first_name} {user.last_name},
        
            O preço da ação {code} atingiu R${value}, ficando abaixo do valor estipulado para compra.

            Atenciosamente,
            Equipe B3Tracker
        ''',
        "b3tracker@gmail.com",
        [f"{user.email}"],
        fail_silently=False,

    )

def send_mail_upload(user, code):
    
    send_mail(
        f"{code}Adicionada ao BD",
        f'''
            Prezado(a) {user.first_name} {user.last_name},
        
            A ação {code} foi adicionada ao monitoramento.
            
            Atenciosamente,
            Equipe B3Tracker
        ''',
        "b3tracker@gmail.com",
        [f"{user.email}"],
        fail_silently=False,

    )

def monitoring(user , code):
    
    while True:
        sleep(60)
        ticker = Ticker.objects.get(user = user, ticker=code)
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
                send_mail_sell(user, code , round(value,2))
            if value < ticker.tunnel_inf:
                send_mail_buy(user, code , round(value,2))

def create_monitoring_thread(user, code):
    # Verifica se já existe uma thread em execução para o mesmo ticker
    existing_threads = [thread for thread in threading.enumerate() if thread.name == f"monitoring_thread_{code}_{user.username}"]

    if not existing_threads:
        # Se não houver thread existente, cria uma nova
        
        monitoring_thread = threading.Thread(target=monitoring, args=(user,code), name=f"monitoring_thread_{code}_{user.username}")
        monitoring_thread.start()