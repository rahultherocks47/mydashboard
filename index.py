app_id = 'F8QQEC8OV3-100'
app_secret = '1E0WOPB0EV'

redirect_url = 'https://www.google.com'

from fyers_api import fyersModel,accessToken
import os
import requests
# url = 'https://api.fyers.in/api/v2/token'
# requestParams = {
#fyers_id = "XG08763",
# "password":"123$rocK",
# "pan_dob":"EGYPR7128J",
# "appId": app_id,
# "create_cookie":False}
# response = requests.post(url, json = requestParams )
# print (response.text)

def get_access_token():
    if not os.path.exists("access_token.txt"):
        session=accessToken.SessionModel(client_id=app_id,
        secret_key=app_secret,redirect_uri=redirect_url, 
        response_type='code', grant_type='authorization_code')
        response = session.generate_authcode()  
        print("LOGIN URL : ", response )
        auth_code =input("ENTER AUTH CODE:")
        session.set_token(auth_code)
        print("SESSION")
        access_token =session.generate_token()['access_token']
        print(access_token)
        with open("access_token.txt",'w') as f:
           f.write(access_token)        
    else:
        with open('access_token.txt','r') as f:
            access_token = f.read()
    return access_token

fyers = fyersModel.FyersModel(client_id=app_id, token=get_access_token(),log_path="")
data = {"symbol":"NSE:SBIN-EQ","resolution":"D","date_format":"1","range_from":"2022-05-01","range_to":"2022-05-13","cont_flag":"1"}
historical_data = fyers.history(data)
for candle in historical_data['candles']:
    print(candle)



# https://api.fyers.in/api/v2/generate-authcode?
# client_id=SPXXXXE7-100&
# redirect_uri=https%3A%2F%2Fdev.fyers.in%2Fredirection%2Findex.html
# &response_type=code&state=sample_state&nonce=sample_nonce
