from django.shortcuts import render, redirect, reverse
import pandas as pd
import requests
from .models import Exchange, Company
import time
from project import settings
from django.db import connection
from django.core.management import call_command

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
    """
    Delete all companies in DB and loas them from API; rebuild elasticserach index
    """
    #Company.objects.all().delete() - this is too slow, alternative with sql is fast
    print('Starting sql for delete')
    cursor = connection.cursor()
    sql = "TRUNCATE TABLE finhub_company;"
    cursor.execute(sql)
    print('all companies are deleted')
    print('starting update via API calls')
    size = len(Exchange.objects.all())
    counter = 1
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
        print('Updated {}. Record {} of {}'.format(exchange_record, counter, size))
        time.sleep(1)
        counter = counter + 1
    print('startig elasticsearch index create')
    call_command('search_index', '--rebuild', '-f')
    return redirect('exchange')

def exchange_code(request, code):
    """
    Executed when visiting finhub/exchange/<str:code>/
    If no records in DB about thsi stocke exchange will load data from API,
    otherwise will load data from DB and render to template which allows certain
    company to be selected -> redirects to company_details/<int:id>/
    """
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
    """
    Executed when visiting url finhub/exchange/<str:code>/update/
    Delete all records in DB for certain stock exchange and redirects to finhub/exchange/<str:code>/
    """
    exchange_record = Exchange.objects.get(code=code)
    Company.objects.filter(exchange=exchange_record).delete()
    return redirect('exchange_code', code=code)