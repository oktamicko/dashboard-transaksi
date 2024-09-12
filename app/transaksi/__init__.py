from flask import Blueprint

# Inisialisasi blueprint 'transaksi'
transaksi = Blueprint('transaksi', __name__)

# Import routes agar dikenali oleh blueprint ini
from app.transaksi import routes
