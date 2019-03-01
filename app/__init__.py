from flask import Flask
from app.api.v1.database import db_init
from app.api.v1.views.user_view import user_blueprint
def start_app(app_config):
    app = Flask(__name__)
    app.config.from_object([app_config])
    app.register_blueprint(user_blueprint)
    db_init
    return app
