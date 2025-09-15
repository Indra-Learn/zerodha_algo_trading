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


def market_analysis_html_data():
    html_data = dict()

    # Generic html_data
    html_data["brand"] = {"name": "TheDataFestAI", "href": "home.home"}
    html_data["page_title"] = "Market Analysis"  # Trading Llama
    html_data["sidebar_menu_header"] = "TDF's " + html_data["page_title"]
    html_data["current_date"] = get_date_dict().get("cur_date", "Date is missing ..")

    # Primary html_data
    html_data["topnavbar"] = list()
    html_data["topnavbar"].append({"menu": "Products", "href": "#", "sub_menu": ["Market Analysis", "div", "Others"]})
    html_data["topnavbar"].append({"menu": "Services", "href": "#", "sub_menu": ["APIs"]})
    html_data["topnavbar"].append({"menu": "Pricing", "href": "#", "sub_menu": []})
    html_data["topnavbar"].append({"menu": "Blogs/Docs", "href": "#", "sub_menu": []})

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
    html_data["sidebar"].append({"menu": "Trading Acronyms", "icon": "fas fa-search me-2", "href": "products_services.market_analysis.trading_acronyms", "sub_menu": []})
    html_data["sidebar"].append({"menu": "Knowledge / Docs", "icon": "fas fa-file me-2", "href": "products_services.market_analysis.docs", "sub_menu": []})
    
    html_data["user"] = None
    return html_data


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
    html_data = market_analysis_html_data()
    html_data["main_content_header"] = html_data["sidebar"][0].get("menu")

    # Page Specific html_data
    nse_api = NSE_APIS()
    # df = nse_api.get_historic_daily_data(symbol="BLUESTONE", from_dt="10-09-2024", to_dt="10-09-2025")
    # html_data["chart_symbol"] = create_candlestick_chart(df, "BLUESTONE")
    html_data["overall_market_status"] = ""
    html_data["market_analysis_top_states"] = [{"name": "Nifty", "ltp": "", "perchange": ""},
                                               {"name": "Sensex", "ltp": "", "perchange": ""},
                                               {"name": "USD-INR Rate", "ltp": "", "perchange": ""},
                                               {"name": "Crude Oil", "ltp": "", "perchange": ""},
                                               {"name": "India VIX", "ltp": "", "perchange": ""},
                                               {"name": "Bitcoin", "ltp": "", "perchange": ""}]
    
    df1 = nse_api.get_daily_allIndices_data()
    html_data["top_5_indices_df"] = df1[df1['Index'].isin(['NIFTY 50', 'NIFTY NEXT 50', 'NIFTY BANK', 'NIFTY MIDCAP 150', 'NIFTY SMALLCAP 250'])]
    html_data["fii_dii_df"] = nse_api.get_daily_fii_dii_data()    
    
    return render_template("products_services/market_analysis/market_trends.html", html_data=html_data)


@market_analysis_bp.route("/acronyms", methods=['GET'])
def trading_acronyms():
    html_data = market_analysis_html_data()
    html_data["main_content_header"] = "Trading Acronyms"

    return render_template("products_services/market_analysis/trading_acronyms.html", html_data=html_data)


@market_analysis_bp.route("/docs", methods=['GET'])
def docs():
    html_data = market_analysis_html_data()
    return render_template("products_services/market_analysis/test.html", html_data=html_data)