import os
import sys
import logging
import requests
from flask import Blueprint, abort
from flask import request, render_template, redirect, url_for, session, flash
from functools import wraps
from kiteconnect import KiteConnect

logging.basicConfig(level=logging.DEBUG)

parentdir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(parentdir)


from utils.tdf_admin import get_admin_secret, get_kite_secret

kite_secret = get_kite_secret()

home_bp = Blueprint('home', __name__, 
                    template_folder='templates',
                    static_folder='static',
                    url_prefix='/')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('Please log in to access this page.', 'danger')
            return redirect(url_for('home.login'))
        return f(*args, **kwargs)
    return decorated_function

def get_kite_client():
    kite = KiteConnect(api_key=kite_secret["api_key"])
    if "kite_access_token" in session:
        kite.set_access_token(session["kite_access_token"])
    return kite

@home_bp.route('/login', methods=['GET', 'POST'])
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
    return redirect(url_for('home.home'))

@home_bp.route('/logout')
def logout():
    # Clear the session
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home.home'))

# Home Page
@home_bp.route("/", methods=['GET'])
def home():
    return render_template('home/home.html', html_data={})

# Kite Login
@home_bp.route("/kitelogin")
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


@home_bp.route("/holdings")
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

@home_bp.route('/ticker')
@login_required
def ticker():
    return render_template('base.html', active_page='ticker', html_data={})
