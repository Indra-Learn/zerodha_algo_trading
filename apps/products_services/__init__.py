from flask import Blueprint

products_services_bp = Blueprint('products_services', __name__, 
                template_folder='templates',
                static_folder='static',
                url_prefix='/products_services')