from flask import Blueprint

products_services_bp = Blueprint('products_services', __name__, 
                template_folder='templates',
                static_folder='static',
                url_prefix='/products_services')

from apps.products_services.portfolio_tracker import portfolio_tracker_bp

# Register sub-blueprints with the main product blueprint
products_services_bp.register_blueprint(portfolio_tracker_bp, url_prefix='/portfolio_tracker')

from apps.products_services.portfolio_tracker import routes