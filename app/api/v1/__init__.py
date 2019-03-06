from flask import Flask, Blueprint

app_blueprint = Blueprint("app", __name__, url_prefix='/api/v1')