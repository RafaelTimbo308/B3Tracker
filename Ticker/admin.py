from django.contrib import admin
from .models import Ticker
# Register your models here.

class TickerAdmin(admin.ModelAdmin):
    
    list_display = ('user','ticker','value','tunnel_inf','tunnel_sup', 'interval', 'last_update')
    
admin.site.register(Ticker,TickerAdmin)