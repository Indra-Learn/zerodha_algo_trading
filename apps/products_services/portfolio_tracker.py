import os
import sys
import logging
import requests
from flask import Blueprint, abort
from flask import request, render_template, redirect, url_for, session
from kiteconnect import KiteConnect

logging.basicConfig(level=logging.DEBUG)

parentdir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir))
sys.path.append(parentdir)

from apps.products_services import products_services_bp
from config import dev_config
from utils.tdf_admin import get_kite_secret

HOST = dev_config["host"] 
PORT = dev_config["port"]
kite_secret = get_kite_secret()

# @products_services_bp.route("/", methods=['GET'])
# def portfolio_tracker_home():
#     return render_template("products_services/ps_home.html", html_data={})

portfolio_tracker_bp = Blueprint('portfolio_tracker', __name__, 
                template_folder='templates',
                static_folder='static',
                url_prefix='/portfolio_tracker')

@products_services_bp.route("/", methods=['GET'])
def portfolio_tracker_home():
    kite_login = False
    html_data={}
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
    return render_template("products_services/ps_home.html", html_data=html_data)