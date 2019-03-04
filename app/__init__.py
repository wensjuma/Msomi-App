from flask import Flask

from instance.config import config

from app.api.v1.views.profile_view import profile_blueprint


def start_app(app_config):
    app = Flask(__name__)

    app.config.from_object(config[app_config])

    app.register_blueprint(profile_blueprint)

    from app.api.v1.views.group_view import group_blueprints 
    app.register_blueprint(group_blueprints)

    return app
