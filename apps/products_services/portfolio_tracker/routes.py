import os
import sys
import logging
import requests
from flask import abort
from flask import request, render_template, redirect, url_for, session
from kiteconnect import KiteConnect
import pandas as pd

# logging.basicConfig(level=logging.DEBUG)

parentdir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir))
sys.path.append(parentdir)

from apps.products_services.portfolio_tracker import portfolio_tracker_bp
from config import dev_config
from utils.tdf_admin import get_kite_secret
# from utils.stock_apis import get_data_from_kite_api
from apps.home import login_required

HOST = dev_config["host"] 
PORT = dev_config["port"]
kite_secret = get_kite_secret()

def get_kite_client():
    kite = KiteConnect(api_key=kite_secret["api_key"])
    if "kite_access_token" in session:
        kite.set_access_token(session["kite_access_token"])
    return kite

@portfolio_tracker_bp.route("/", methods=['GET'])
@login_required
def portfolio_tracker_home():
    kite_login = False
    html_data={}
    transformed_mf_df=pd.DataFrame()
    html_data["login_url"] = "https://kite.zerodha.com/connect/login?api_key={api_key}".format(api_key=kite_secret["api_key"])
    html_data["redirect_url"] = "http://{host}:{port}/kitelogin".format(host=HOST, port=PORT)
    html_data["console_url"] = "https://developers.kite.trade/apps/{api_key}".format(api_key=kite_secret["api_key"])

    if "username" in session:
        html_data["username"] = session.get("username")
        if "kite_access_token" in session:
            kite_login = True
            html_data["kite_user_type"] = session.get("kite_user_type")
            html_data["kite_email"] = session.get("kite_email")
            html_data["kite_user_name"] = session.get("kite_user_name")
            html_data["kite_user_id"] = session.get("kite_user_id")
            html_data["kite_avatar_url"] = session.get("kite_avatar_url")
            html_data["kite_broker"] = session.get("kite_broker")
            # html_data["list_mf"] = []
            kite = get_kite_client()
            mf_df = pd.DataFrame(kite.mf_instruments())
            transformed_mf_df = mf_df.loc[(mf_df["purchase_allowed"]==True) 
                                          & (mf_df["dividend_type"]=="growth")
                                          & (mf_df["plan"]=="direct"), 
                                          ["amc", "name", "scheme_type", "last_price", "last_price_date" ]]
    return render_template("products_services/portfolio_tracker/home.html", kite_login=kite_login, 
                           html_data=html_data, mf_df=transformed_mf_df)

# Kite Login
@portfolio_tracker_bp.route("/kitelogin")
@login_required
def kite_login():
    kite_request_token = request.args.get("request_token")
    if not kite_request_token:
        return """
            <span style="color: red">
                Error while generating request token.
            </span>
            <a href='/'>Try again.<a>"""
    kite = get_kite_client()
    kite_login_data = kite.generate_session(kite_request_token, api_secret=kite_secret["api_secret"])
    session["kite_access_token"] = kite_login_data.get("access_token")
    session["kite_user_type"] = kite_login_data.get("user_type")
    session["kite_email"] = kite_login_data.get("email")
    session["kite_user_name"] = kite_login_data.get("user_name")
    session["kite_user_id"] = kite_login_data.get("user_id")
    session["kite_avatar_url"] = kite_login_data.get("avatar_url")
    session["kite_broker"] = kite_login_data.get("broker")
    # '<h1>Welcome to Login Page</h1><p><a href="/">Click Here</a> to back to Home Page</p>'
    return redirect(url_for('products_services.portfolio_tracker.portfolio_tracker_home'))


# @portfolio_tracker_bp.route("/holdings")
# @login_required
# def holdings():
#     kite_headers = {
#         "X-Kite-Version": "3",
#         "Authorization": f"token {kite_secret["api_key"]}:{session.get("kite_access_token")}"
#     }
#     response = requests.get(url="https://api.kite.trade/portfolio/holdings", headers=kite_headers)
#     response.raise_for_status()
#     data = response.json()
#     return data["data"]