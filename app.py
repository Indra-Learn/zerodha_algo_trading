"""
https://github.com/zerodha/pykiteconnect/blob/master/examples/flask_app.py
"""

import os
import sys
import logging
import requests
from flask import Flask, render_template, session, request
from kiteconnect import KiteConnect

logging.basicConfig(level=logging.DEBUG)

parentdir = os.path.abspath(os.path.join(os.path.dirname(__file__)))
sys.path.append(parentdir)

from config import dev_config
from utils.kite_api import get_kite_secret

app = Flask(__name__)
app.secret_key = os.urandom(24)  # required for flask-session

HOST = dev_config["host"] 
PORT = dev_config["port"]
kite_secret = get_kite_secret()

def get_kite_client():
    kite = KiteConnect(api_key=kite_secret["api_key"])
    if "kite_access_token" in session:
        kite.set_access_token(session["kite_access_token"])
    return kite

# Home Page
@app.route("/")
def home():
    kite_login = False
    html_data = {}
    html_data["login_url"] = "https://kite.zerodha.com/connect/login?api_key={api_key}".format(api_key=kite_secret["api_key"])
    html_data["redirect_url"] = "http://{host}:{port}/login".format(host=HOST, port=PORT)
    html_data["console_url"] = "https://developers.kite.trade/apps/{api_key}".format(api_key=kite_secret["api_key"])
    
    if "kite_access_token" in session:
        kite_login = True
        html_data["kite_user_type"] = session.get("kite_user_type")
        html_data["kite_email"] = session.get("kite_email")
        html_data["kite_user_name"] = session.get("kite_user_name")
        html_data["kite_user_id"] = session.get("kite_user_id")
        html_data["kite_avatar_url"] = session.get("kite_avatar_url")
        html_data["kite_broker"] = session.get("kite_broker")
    return render_template('home/home.html', kite_login=kite_login, html_data=html_data)

# Kite Login
@app.route("/login")    
def login():
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
    return '<h1>Welcome to Login Page</h1><p><a href="/">Click Here</a> to back to Home Page</p>'


@app.route("/holdings")
def holdings():
    kite_headers = {
        "X-Kite-Version": "3",
        "Authorization": f"token {kite_secret["api_key"]}:{session.get("kite_access_token")}"
    }
    response = requests.get(url="https://api.kite.trade/portfolio/holdings", headers=kite_headers)
    response.raise_for_status()
    data = response.json()
    return data["data"]


@app.route('/index')
def index():
    return render_template('base.html')

@app.route('/trade')
def trade():
    return render_template('base.html', active_page='trade')

@app.route('/ticker')
def ticker():
    return render_template('base.html', active_page='ticker')

if __name__ == "__main__":
    HOST = dev_config["host"]
    PORT = dev_config["port"]
    logging.info("Starting server: http://{host}:{port}".format(host=HOST, port=PORT))
    app.run(host=HOST, port=PORT, debug=True)