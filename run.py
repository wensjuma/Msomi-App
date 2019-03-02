import os
from flask import Flask
from app import start_app
app = start_app(os.getenv('FLASK_ENV'))

if __name__ == "__main__":   
    app.run(debug=True)