# Gunakan base image Python 3.12
FROM python:3.12

# Atur environment variables untuk meningkatkan kinerja Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Buat direktori kerja
WORKDIR /app

# Salin file requirements.txt ke direktori kerja
COPY requirements.txt .

# Instal dependencies dari requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Salin kode aplikasi ke direktori kerja
COPY . .

# Ekspos port yang digunakan oleh aplikasi Flask
EXPOSE 5000

# Tetapkan perintah untuk menjalankan aplikasi dengan Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5010", "run:app"]
