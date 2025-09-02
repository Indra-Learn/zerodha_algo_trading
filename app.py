"""
https://github.com/zerodha/pykiteconnect/blob/master/examples/flask_app.py
"""

import os
import sys
import logging
import requests
from flask import Flask, request, render_template, redirect, url_for, session, flash
from functools import wraps
from kiteconnect import KiteConnect

logging.basicConfig(level=logging.DEBUG)

parentdir = os.path.abspath(os.path.join(os.path.dirname(__file__)))
sys.path.append(parentdir)

from config import dev_config
from utils.kite_api import get_kite_secret, get_admin_secret

app = Flask(__name__)
app.secret_key = os.urandom(24)  # required for flask-session

HOST = dev_config["host"] 
PORT = dev_config["port"]
kite_secret = get_kite_secret()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('Please log in to access this page.', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def get_kite_client():
    kite = KiteConnect(api_key=kite_secret["api_key"])
    if "kite_access_token" in session:
        kite.set_access_token(session["kite_access_token"])
    return kite

@app.route('/login', methods=['GET', 'POST'])
def login():
    # If user is already logged in, redirect to home
    if 'username' in session:
        pass
    elif request.method == 'POST':
        username = request.form['loginEmail']
        password = request.form['loginPassword']
        # Check if user exists and password matches
        admin_secret = get_admin_secret()
        if username == admin_secret.get("userid") and password == admin_secret.get("password"):
            # Set session variables
            session['username'] = username
            flash('Login successful!', 'success')
        else:
            flash('Invalid username or password. Please try again.', 'danger')
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    # Clear the session
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

# Home Page
@app.route("/")
def home():
    kite_login = False
    html_data = {}
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
    return render_template('home/home.html', kite_login=kite_login, html_data=html_data)

# Kite Login
@app.route("/kitelogin")
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
    return '<h1>Welcome to Login Page</h1><p><a href="/">Click Here</a> to back to Home Page</p>'


@app.route("/holdings")
@login_required
def holdings():
    kite_headers = {
        "X-Kite-Version": "3",
        "Authorization": f"token {kite_secret["api_key"]}:{session.get("kite_access_token")}"
    }
    response = requests.get(url="https://api.kite.trade/portfolio/holdings", headers=kite_headers)
    response.raise_for_status()
    data = response.json()
    return data["data"]

@app.route('/trade')
@login_required
def trade():
    return render_template('base.html', active_page='trade')

@app.route('/ticker')
@login_required
def ticker():
    return render_template('base.html', active_page='ticker')

if __name__ == "__main__":
    HOST = dev_config["host"]
    PORT = dev_config["port"]
    logging.info("Starting server: http://{host}:{port}".format(host=HOST, port=PORT))
    app.run(host=HOST, port=PORT, debug=True)