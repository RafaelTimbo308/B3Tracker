#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from django.db.backends.signals import connection_created
from django.dispatch import receiver

@receiver(connection_created)
def on_connection_created(sender, **kwargs):
    from Ticker.tasks import create_monitoring_thread
    from Ticker.models import Ticker
    # Esta função será chamada assim que a conexão com o banco de dados for criada
    tickers = Ticker.objects.all()
    for ticker in tickers:
        create_monitoring_thread(ticker.ticker) 
    
def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'B3Tracker.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
