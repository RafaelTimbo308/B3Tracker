from django.contrib import admin
from .models import Ticker
# Register your models here.

class TickerAdmin(admin.ModelAdmin):
    
    list_display = ('ticker','value')
    
admin.site.register(Ticker,TickerAdmin)