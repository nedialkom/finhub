from django.urls import path

from . import views

urlpatterns = [
    path('', views.finhub, name='finhub'),
    path('exchange/', views.exchange, name='exchange'),
    path('exchange/load', views.load_companies, name='load_companies'),
    path('exchange/<str:code>/', views.exchange_code, name='exchange_code'),
    path('exchange/<str:code>/update/', views.exchange_update, name='exchange_update'),
]