import pymysql
from flask import current_app

# Fungsi untuk mendapatkan koneksi ke database
def get_db_connection():
    connection = pymysql.connect(
        host=current_app.config['DB_HOST'],
        user=current_app.config['DB_USER'],
        password=current_app.config['DB_PASSWORD'],
        database=current_app.config['DB_NAME']
    )
    return connection
