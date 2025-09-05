"""
https://github.com/zerodha/pykiteconnect/blob/master/examples/flask_app.py
https://kite.trade/docs/pykiteconnect/v4/
"""
import os
import logging
# from kiteconnect import KiteConnect
import requests

# logging.basicConfig(level=logging.DEBUG)

    
def _get_data_from_kite_api(self, api_endpoint_url, kite_api_key, kite_access_token):
    kite_root_url = "https://api.kite.trade"
    kite_headers = {
        "X-Kite-Version": "3",
        "Authorization": f"token {kite_api_key}:{kite_access_token}"
    }
    full_kite_url = kite_root_url + "/" + api_endpoint_url
    response = requests.get(url=full_kite_url, headers=kite_headers)
    response.raise_for_status()
    data = response.json()
    return data["data"]




