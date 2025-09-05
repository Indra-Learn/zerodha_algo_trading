from flask import Blueprint

portfolio_tracker_bp = Blueprint('portfolio_tracker', __name__,
                template_folder='templates',
                static_folder='static')

# Import routes after creating the blueprint to avoid circular imports
from apps.products_services.portfolio_tracker import routes