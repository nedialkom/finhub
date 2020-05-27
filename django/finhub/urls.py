from django.urls import path

from . import views

urlpatterns = [
    path('', views.finhub, name='finhub'),
]