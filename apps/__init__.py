import os, sys
from flask import Flask

parentdir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(parentdir)

from config import dev_config

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY = os.urandom(24),  # required for flask-session
        # DATABASE = os.path.join(app.instance_path, 'apps.sqlite')
    )
    
    # Register blueprints
    from . import home, blogs, products_services
    from .products_services import portfolio_tracker
    app.register_blueprint(home.home_bp)
    app.register_blueprint(products_services.products_services_bp)
    app.register_blueprint(blogs.blogs_bp)
    
    return app

app = create_app()

if __name__ == "__main__":
    HOST = dev_config["host"]
    PORT = dev_config["port"]
    app.run(host=HOST, port=PORT, debug=True)
