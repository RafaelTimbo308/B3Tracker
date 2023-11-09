from django.db import models

# Create your models here.

class Ticker(models.Model):
    
    ticker = models.CharField(primary_key=True , max_length=8)
    tunnel_inf = models.DecimalField(decimal_places=2 , max_digits=6)
    tunnel_sup = models.DecimalField(decimal_places=2 , max_digits=6)
    value = models.DecimalField(decimal_places=2 , max_digits=6,)
    interval = models.IntegerField(default=5)
    last_update = models.DateTimeField()
