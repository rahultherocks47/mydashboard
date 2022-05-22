from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Stock
from .utils import get_access_token, syncStocksData,get_stock_data


# Create your views here.
@api_view(['GET'])
def getRoutes(request):
    routes = [
        {
            'Endpoint': '/syncdata/',
            'method': 'GET',
            'body': None,
            'description': 'Returns an array of latest ohlcv data of given stocks'
        },
        {
            'Endpoint': '/stock/symbol/',
            'method': 'GET',
            'body': None,
            'description': 'Returns an array of latest ohlcv data of given stocks'
        },
    ]
    return Response(routes)

@api_view(['GET'])
def syncData(request):
    if request.method == "GET":
        return syncStocksData(request)   

@api_view(['GET'])
def connectFyer(request):
    if request.method == "GET":
        return get_access_token(request)

@api_view(['GET'])
def showStock(request,symbol):
    if request.method == "GET":
        return get_stock_data(request,symbol)  