import os
import sys
import logging
import requests
from flask import Blueprint, abort
from flask import request, render_template, redirect, url_for, session, flash
from functools import wraps
from kiteconnect import KiteConnect

# logging.basicConfig(level=logging.DEBUG)

parentdir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(parentdir)

from utils.tdf_admin import get_admin_secret

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
    html_data = {}
    if 'username' in session:
        html_data["username"] = session.get("username")
    return render_template('home/home.html', html_data=html_data)

@home_bp.route('/ticker')
@login_required
def ticker():
    return render_template('base.html', active_page='ticker', html_data={})
