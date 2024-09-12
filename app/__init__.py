from flask import Flask
from app.db import get_db_connection
from app.main import main as main_blueprint
from app.transaksi import transaksi as transaksi_blueprint

def create_app():
    app = Flask(__name__)

    # Konfigurasi aplikasi
    app.config.from_pyfile('../config.py')

    # Register blueprints
    app.register_blueprint(main_blueprint, url_prefix='/main')
    app.register_blueprint(transaksi_blueprint, url_prefix='/transaksi')

    return app
