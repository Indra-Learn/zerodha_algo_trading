from flask import Blueprint

products_services_bp = Blueprint('products_services', __name__, 
                template_folder='templates',
                static_folder='static',
                url_prefix='/products_services')

from apps.products_services.market_analysis import market_analysis_bp
from apps.products_services.portfolio_tracker import portfolio_tracker_bp

# Register sub-blueprints with the main product blueprint
products_services_bp.register_blueprint(portfolio_tracker_bp, url_prefix='/portfolio_tracker')
products_services_bp.register_blueprint(market_analysis_bp, url_prefix='/market_analysis')

from apps.products_services.market_analysis import routes
from apps.products_services.portfolio_tracker import routes