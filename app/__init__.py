from flask import Flask

from instance.config import config

from app.api.v1.views.user_view import user_blueprint

def start_app(app_config):
    app = Flask(__name__)

    app.config.from_object(config[app_config])

    app.register_blueprint(user_blueprint)

    return app
