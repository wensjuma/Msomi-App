import os
from app import start_app
app= start_app('FLASK_ENV')

if __name__ == "__main__":   
    app.run(debug=True)