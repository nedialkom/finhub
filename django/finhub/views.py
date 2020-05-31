from django.shortcuts import render, redirect, reverse
import pandas as pd
import requests
from .models import Exchange, Company
import time
from project import settings

API_KEY = settings.FINNHUB_API_KEY
END_POINT = 'https://finnhub.io/api/v1'

def finhub(request):
    return render(request, 'finhub/finhub.html')

def exchange(request):
    # Initial load from excel file
    if Exchange.objects.count() == 0:
        df = pd.read_excel('exchanges.xlsx')
        Exchange.objects.bulk_create(
            Exchange(**vals) for vals in df.to_dict('records')
        )
    context = {'context':Exchange.objects.all()}
    return render(request, 'finhub/exchange.html', context)

def load_companies(request):
    Company.objects.all().delete()
    API = '/stock/symbol?exchange='
    for exchange_record in Exchange.objects.all():
        url = END_POINT + API + exchange_record.code + '&token=' + API_KEY
        r = requests.get(url)
        df = pd.DataFrame(r.json())
        df_records = df.to_dict('records')
        model_instances = [Company(
            description=record['description'],
            displaySymbol=record['displaySymbol'],
            symbol=record['symbol'],
            exchange = exchange_record,
        ) for record in df_records]
        Company.objects.bulk_create(model_instances)
        time.sleep(1)
    return redirect('exchange')

def exchange_code(request, code):
    exchange_record = Exchange.objects.get(code=code)
    API = '/stock/symbol?exchange='
    url = END_POINT + API + exchange_record.code + '&token=' + API_KEY
    r = requests.get(url)
    if len(Company.objects.filter(exchange=exchange_record))== 0:
        df = pd.DataFrame(r.json())
        df_records = df.to_dict('records')
        model_instances = [Company(
            description=record['description'],
            displaySymbol=record['displaySymbol'],
            symbol=record['symbol'],
            exchange = exchange_record,
        ) for record in df_records]
        Company.objects.bulk_create(model_instances)
    stocks = Company.objects.filter(exchange=exchange_record)
    context = {'exchange':exchange_record, 'stocks':stocks}
    return render(request, 'finhub/exchange_code.html', context)

def exchange_update(request, code):
    exchange_record = Exchange.objects.get(code=code)
    Company.objects.filter(exchange=exchange_record).delete()
    return redirect('exchange_code', code=code)