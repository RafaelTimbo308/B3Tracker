from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home , name = 'home'),
    path('Detail/', views.Detail , name = 'details'),
]
