import os
import sys
import logging
import pandas as pd
from flask import abort
from flask import request, render_template, redirect, url_for, session

# logging.basicConfig(level=logging.DEBUG)

parentdir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir, os.path.pardir))
sys.path.append(parentdir)

from apps.products_services.market_analysis import market_analysis_bp

from utils.stock_apis import get_mf_instrument, kite_api_key
from utils.nse_apis import NSE_APIS
from apps.home import login_required

@market_analysis_bp.route("/", methods=['GET'])
@login_required
def market_analysis_home():
    html_data = {}
    large_deal_df = NSE_APIS().get_large_deal_data()
    large_deal_html = large_deal_df.to_html(header="true", table_id="table", 
                                            classes='dataframe', index=False, 
                                            escape=False)
    html_data["large_deal_html"] = large_deal_html
    if "username" in session:
        html_data["username"] = session.get("username")
        if "kite_access_token" in session:
            mf_instrument_df = get_mf_instrument()
            mf_instrument_html = mf_instrument_df.to_html(header="true", table_id="table", 
                                                          classes='dataframe', index=False, 
                                                          escape=False)
            html_data["mf_instrument_html"] = mf_instrument_html
    return render_template("products_services/market_analysis/home.html", html_data=html_data)