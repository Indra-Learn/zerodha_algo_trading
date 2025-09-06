from flask import Blueprint

market_analysis_bp = Blueprint('market_analysis', __name__,
                template_folder='templates',
                static_folder='static')

# Import routes after creating the blueprint to avoid circular imports
from apps.products_services.market_analysis import routes