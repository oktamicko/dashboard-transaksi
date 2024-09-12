from flask import render_template, request, redirect, url_for
from app.db import get_db_connection
from app.transaksi import transaksi

@transaksi.route('/', methods=['GET', 'POST'])
def transaksi_page():
    connection = get_db_connection()
    cursor = connection.cursor()

    # Ambil data anggota dan admin dari database
    cursor.execute("SELECT id, name FROM anggota")
    anggota_list = cursor.fetchall()

    cursor.execute("SELECT id, name FROM admin")
    admin_list = cursor.fetchall()

    if request.method == 'POST':
        # Ambil data dari form
        anggota_id = request.form['anggota_id']
        admin_id = request.form['admin_id']
        nama_barang = request.form['nama_barang']
        quantity = int(request.form['quantity'])
        harga = float(request.form['harga'])
        total = quantity * harga

        # Masukkan transaksi ke dalam database
        cursor.execute("""
            INSERT INTO transaksi (anggota_id, admin_id, nama_barang, quantity, harga, total)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (anggota_id, admin_id, nama_barang, quantity, harga, total))
        connection.commit()

        return redirect(url_for('transaksi.transaksi_page'))

    # Ambil semua transaksi untuk ditampilkan
    cursor.execute("""
        SELECT t.id, a.name AS anggota_name, ad.name AS admin_name, t.nama_barang, t.quantity, t.harga, t.total
        FROM transaksi t
        JOIN anggota a ON t.anggota_id = a.id
        JOIN admin ad ON t.admin_id = ad.id
    """)
    transaksi_list = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template('transaksi/transaksi.html', anggota_list=anggota_list, admin_list=admin_list, transaksi_list=transaksi_list)

# Fungsi delete transaksi
@transaksi.route('/delete/<int:id>', methods=['POST'])
def delete_transaksi(id):
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM transaksi WHERE id = %s", (id,))
    connection.commit()
    cursor.close()
    connection.close()

    return redirect(url_for('transaksi.transaksi_page'))

# Fungsi edit transaksi
@transaksi.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_transaksi(id):
    connection = get_db_connection()
    cursor = connection.cursor()

    if request.method == 'POST':
        anggota_id = request.form['anggota_id']
        admin_id = request.form['admin_id']
        nama_barang = request.form['nama_barang']
        quantity = int(request.form['quantity'])
        harga = float(request.form['harga'])
        total = quantity * harga

        cursor.execute("""
            UPDATE transaksi
            SET anggota_id = %s, admin_id = %s, nama_barang = %s, quantity = %s, harga = %s, total = %s
            WHERE id = %s
        """, (anggota_id, admin_id, nama_barang, quantity, harga, total, id))
        connection.commit()

        return redirect(url_for('transaksi.transaksi_page'))

    # Ambil data transaksi yang akan diedit
    cursor.execute("SELECT anggota_id, admin_id, nama_barang, quantity, harga FROM transaksi WHERE id = %s", (id,))
    transaksi = cursor.fetchone()

    # Ambil daftar anggota dan admin untuk dropdown
    cursor.execute("SELECT id, name FROM anggota")
    anggota_list = cursor.fetchall()

    cursor.execute("SELECT id, name FROM admin")
    admin_list = cursor.fetchall()

    return render_template('transaksi/edit_transaksi.html', transaksi=transaksi, anggota_list=anggota_list, admin_list=admin_list, id=id)
