from app import create_app

app = create_app()
app.config['SECRET_KEY'] = 'supersecretkey123'

if __name__ == "__main__":
    app.run(debug=True)
