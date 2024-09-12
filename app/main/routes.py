from flask import render_template, request, redirect, url_for, flash
from app.db import get_db_connection
from app.main import main

# Route untuk menampilkan form dan list anggota/admin dalam satu halaman
@main.route('/list', methods=['GET', 'POST'])
def list_users():
    role = request.form.get('role', 'anggota')  # Default tampilkan anggota jika tidak ada pilihan

    connection = get_db_connection()
    cursor = connection.cursor()

    # Menampilkan data dari tabel berdasarkan role yang dipilih
    if role == "anggota":
        cursor.execute("SELECT id, name, email FROM anggota")
    elif role == "admin":
        cursor.execute("SELECT id, name, email FROM admin")

    users = cursor.fetchall()
    cursor.close()
    connection.close()
    
    return render_template('main/list_page.html', users=users, role=role)

@main.route('/submit_master', methods=['POST'])
def submit_master():
    # Ambil data dari form
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    role = request.form['role']

    # Koneksi ke database
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        # Masukkan data ke tabel berdasarkan role yang dipilih
        if role == "anggota":
            cursor.execute("INSERT INTO anggota (name, email, password) VALUES (%s, %s, %s)", (name, email, password))
        elif role == "admin":
            cursor.execute("INSERT INTO admin (name, email, password) VALUES (%s, %s, %s)", (name, email, password))
        
        connection.commit()  # Simpan perubahan ke database
        flash(f'{role.capitalize()} berhasil ditambahkan!', 'success')  # Berikan pesan sukses

    except Exception as e:
        connection.rollback()  # Batalkan perubahan jika ada kesalahan
        flash(f'Terjadi kesalahan: {e}', 'danger')  # Berikan pesan kesalahan

    finally:
        cursor.close()
        connection.close()

    return redirect(url_for('main.list_users'))  # Redirect ke halaman daftar pengguna

# Route untuk delete anggota/admin
@main.route('/delete_user/<role>/<int:id>', methods=['POST'])
def delete_user(role, id):
    connection = get_db_connection()
    cursor = connection.cursor()

    # Delete berdasarkan role
    if role == "anggota":
        cursor.execute("DELETE FROM anggota WHERE id = %s", (id,))
    elif role == "admin":
        cursor.execute("DELETE FROM admin WHERE id = %s", (id,))

    connection.commit()
    cursor.close()
    connection.close()

    return redirect(url_for('main.list_users'))

# Route untuk edit anggota/admin
@main.route('/edit_user/<role>/<int:id>', methods=['GET', 'POST'])
def edit_user(role, id):
    connection = get_db_connection()
    cursor = connection.cursor()

    # Jika POST, update data
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        # Update data berdasarkan role
        if role == "anggota":
            cursor.execute("UPDATE anggota SET name = %s, email = %s, password = %s WHERE id = %s", (name, email, password, id))
        elif role == "admin":
            cursor.execute("UPDATE admin SET name = %s, email = %s, password = %s WHERE id = %s", (name, email, password, id))

        connection.commit()
        cursor.close()
        connection.close()

        return redirect(url_for('main.list_users'))

    # Jika GET, tampilkan form edit
    else:
        if role == "anggota":
            cursor.execute("SELECT name, email FROM anggota WHERE id = %s", (id,))
        elif role == "admin":
            cursor.execute("SELECT name, email FROM admin WHERE id = %s", (id,))

        user = cursor.fetchone()
        cursor.close()
        connection.close()

        return render_template('main/edit_user.html', user=user, role=role, id=id)
