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

from utils.python_utils import get_date_dict
from utils.stock_apis import get_mf_instrument, kite_api_key
from utils.nse_apis import NSE_APIS, create_candlestick_chart
from apps.home import login_required

@market_analysis_bp.route("/", methods=['GET'])
# @login_required
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


@market_analysis_bp.route("/trends", methods=['GET'])
def market_analysis_trends():
    """
    http://127.0.0.1:8080/products_services/market_analysis/trends
    """
    html_data = dict()

    # Generic html_data
    html_data["brand"] = {"name": "TheDataFestAI", "href": "home.home"}
    html_data["current_date"] = get_date_dict().get("cur_date", "Date is missing ..")

    # Primary html_data
    html_data["sidebar"] = list()
    html_data["sidebar"].append({"menu": "Market Trends", "icon": "fas fa-chart-line me-2", "href": "products_services.market_analysis.market_analysis_trends", "sub_menu": []})
    html_data["sidebar"].append({"menu": "Portfolio Utility", "icon": "fas fa-table me-2", "href": "#", "sub_menu": [{"name": "Portfolio Tracker", "href": "#"}, 
                                                                                                                    {"name": "Tax Harvesting", "href": "#"},
                                                                                                                    {"name": "Re-balance Portfolio", "href": "#"}]})
    html_data["sidebar"].append({"menu": "Trading Strategies", "icon": "fas fa-bullseye me-2", "href": "#", "sub_menu": [{"name": "India - Stock Market", "href": "#"},
                                                                                                                        {"name": "India - Futures & Options", "href": "#"}, 
                                                                                                                        {"name": "India - Mutual Fund", "href": "#"},
                                                                                                                        {"name": "India - ETF", "href": "#"},
                                                                                                                        {"name": "US - Stock Market", "href": "#"},
                                                                                                                        {"name": "Crypto", "href": "#"}]})
    html_data["sidebar"].append({"menu": "AI Tools", "icon": "fas fa-rocket me-2", "href": "#", "sub_menu": [{"name": "AI ChatBot", "href": "#"}]})
    html_data["sidebar"].append({"menu": "Algo Trading", "icon": "fas fa-robot me-2", "href": "#", "sub_menu": []})
    html_data["sidebar"].append({"menu": "Knowledge / Docs", "icon": "fas fa-file me-2", "href": "#", "sub_menu": []})
    
    # Page Specific html_data
    html_data["page_title"] = "Market Analysis"  # Trading Llama
    html_data["sidebar_menu_header"] = "TDF's " + html_data["page_title"]
    html_data["main_content_header"] = html_data["sidebar"][0].get("menu")
    html_data["overall_market_status"] = ""    
    

    # nse_api = NSE_APIS()
    # df = nse_api.get_historic_daily_data(symbol="BLUESTONE", from_dt="10-09-2024", to_dt="10-09-2025")
    # html_data["chart_symbol"] = create_candlestick_chart(df, "BLUESTONE")
    return render_template("products_services/market_analysis/market_trends.html", html_data=html_data)