from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home , name = 'home'),
    path('cadastro/', views.Cadaster , name='cadaster'),
    path('login/', views.Login , name='login'),
    path('Detail/', views.Detail , name = 'details'),
    path('Remove/<str:code>',views.Delete , name='delete'),
    path('logout/', views.Logout, name='logout')
]
