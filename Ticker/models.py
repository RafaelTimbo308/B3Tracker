from django.db import models
from django.contrib.auth.models import User
import pytz
# Create your models here.

class Ticker(models.Model):
    
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ticker = models.CharField(max_length=5)
    tunnel_inf = models.DecimalField(decimal_places=2 , max_digits=6)
    tunnel_sup = models.DecimalField(decimal_places=2 , max_digits=6)
    value = models.DecimalField(decimal_places=2 , max_digits=6,)
    interval = models.IntegerField(default=5)
    last_update = models.DateTimeField()
    
    class Meta:
        unique_together=['user', 'ticker']
        
    def get_last_update_formatted(self):
        tz = pytz.timezone('America/Sao_Paulo')  # substitua pelo fuso horário desejado
        last_update_localized = self.last_update.replace(tzinfo=pytz.utc).astimezone(tz)
        return last_update_localized.strftime('%d/%m/%Y - %H:%M')