"""
https://github.com/zerodha/pykiteconnect/blob/master/examples/flask_app.py
"""
import os
import logging
# from kiteconnect import KiteConnect
import requests

logging.basicConfig(level=logging.DEBUG)

class KiteApi(object):
    kite_root_url = "https://api.kite.trade"

    def __init__(self, kite_api_key, kite_access_token):        
        self.kite_headers = {
            "X-Kite-Version": "3",
            "Authorization": f"token {kite_api_key}:{kite_access_token}"
        }
    
    def get_data_from_api(self, api_endpoint_url):
        full_kite_url = KiteApi.kite_root_url + "/" + api_endpoint_url
        response = requests.get(url=full_kite_url, headers=self.kite_headers)
        response.raise_for_status()
        data = response.json()
        return data["data"]

