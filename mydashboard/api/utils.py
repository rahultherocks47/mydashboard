from rest_framework.response import Response
from .models import Stock
from .serializer import StockSerializer
from django.conf.urls.static import static
from fyers_api import fyersModel,accessToken
import os
import csv
import requests
from urllib.parse import urlparse, parse_qs
import json
import time
import pandas as pd

app_id = 'F8QQEC8OV3-100'
app_secret = '1E0WOPB0EV'
redirect_url = 'http://localhost:8000/auth'

def get_stock_data(request,symbol):
    fyers = fyersModel.FyersModel(client_id=app_id, token=get_access_token(request),log_path="")
    data = {"symbol": symbol,"resolution":"D","date_format":"1","range_from":"2022-04-01","range_to":"2022-05-17","cont_flag":"1"}
    historical_data = fyers.history(data)
    df = pd.DataFrame.from_dict(historical_data['candles'])
    df.columns=['time','open','high','low','close','volume']
    # df['time'] = pd.to_datetime(df['time'],unit='s')
    # df['time'] = df['time'].dt.tz_localize("utc").dt.tz_convert("Asia/Kolkata")
    # df['time'] = df['time'].dt.tz_localize(None)             
    print(df.to_dict('records'))
    #rows_list = [[row.time,row.open,row.high,row.low,row.close,row.volume] for index,row in df.iterrows()]
    #print(json.dumps(rows_list))    
    return Response(df.to_dict('records'))

def syncStocksData(request):
    stocks_list = list()
    final_list= list()
    df = pd.DataFrame()
    if os.path.exists("static/data.csv"):
        with open("static/data1.csv", "r") as csv_file:
            csvfile = csv.reader(csv_file, delimiter=",")
            stocks_list = [row[0] for row in csvfile]
        fyers = fyersModel.FyersModel(client_id=app_id, token=get_access_token(request),log_path="")
        for stock in stocks_list:
            data = {"symbol": stock,"resolution":"D","date_format":"1","range_from":"2022-05-01","range_to":"2022-05-13","cont_flag":"1"}
            historical_data = fyers.history(data)            
            for candle in historical_data['candles']:
                candle.insert(0,stock)
                final_list.append(candle)
            print(final_list)
        df = pd.DataFrame(final_list,columns = ['symbol' , 'date', 'open' , 'high', 'low', 'close', 'volume'])                
        print(df)
        return Response("data")
    else:
        return Response("no-data")

def get_access_token(request):    
    todayDate = time.strftime("%d-%m-%Y")    
    if not os.path.exists("static/token_"+todayDate + ".txt"):   
        with open("static/appid_key.json") as f:
            data = json.load(f)
        username = data["username"]       # fyers_id
        password = data["password"]        # fyers_password
        pin = int(data["pin"])
        client_id = data["App_Id"]
        secret_key = data["Secret_Id"]
        redirect_url = "https://www.google.com/"
        application_id = client_id[:-4]  # removes  last 4 '-100' it is as in POST request
        session=accessToken.SessionModel(client_id=client_id,secret_key=secret_key,redirect_uri = redirect_url, response_type = 'code', grant_type= 'authorization_code')
        rs = requests.Session()
        pageone_data = f'{{"fy_id":"{username}","app_id":"2"}}'
        pageone_response = rs.post('https://api.fyers.in/vagator/v1/check_user_status', data=pageone_data)
        responseone = pageone_response.json() #["request_key"]

        pagetwo_data = f'{{"fy_id":"{username}","password":"{password}","app_id":"2","imei":"","recaptcha_token":""}}'

        pagetwo_response = rs.post('https://api.fyers.in/vagator/v1/login', data=pagetwo_data)
        responsetwo = pagetwo_response.json()
        request_key = responsetwo["request_key"]

        print(responsetwo['message'])


        pagethree_data = f'{{"request_key":"{request_key}","identity_type":"pin","identifier":"{pin}","recaptcha_token":""}}'
        pagethree_response = rs.post('https://api.fyers.in/vagator/v1/verify_pin', data=pagethree_data)
        responsetthree = pagethree_response.json()
        #access_token = responsetthree['data']["access_token"]

        print(responsetthree['message'])

        headers = {
                'authorization': f"Bearer {responsetthree['data']['access_token']}",
                'content-type': 'application/json; charset=UTF-8'
            }
        # This header carry authorization information so it is required.

        pagefour_data = f'{{"fyers_id":"{username}","app_id":"{application_id}","redirect_uri":"https://www.google.com","appType":"100","code_challenge":"","state":"None","scope":"","nonce":"","response_type":"code","create_cookie":true}}'
        pagefour_response = rs.post('https://api.fyers.in/api/v2/token', data=pagefour_data, headers=headers)
        responsetfour = pagefour_response.json()
        URL_extracted = responsetfour['Url']

        parsed_URL = urlparse(URL_extracted)
        auth_code = parse_qs(parsed_URL.query)['auth_code'][0] # 0 is the 1st auth_code
        session.set_token(auth_code)
        response = session.generate_token()
        print(response)
        access_token = response["access_token"]
        with open("static/token_"+todayDate + ".txt",'w') as f:
            f.write(access_token)
        log_path = "./logs/Documents/Logs_now/" # Your Logs folder
        fyers = fyersModel.FyersModel(client_id=client_id, token=access_token,log_path= log_path)
        is_async = True  # Set to true in you need async API calls       
    else:
        with open("static/token_"+todayDate + ".txt",'r') as f:
            access_token = f.read()
    return access_token
    
    
    