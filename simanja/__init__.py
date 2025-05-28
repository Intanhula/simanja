from flask import Flask
from simanja.config import Config
from simanja.urls import register_routes, item_routes

def simanja():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.secret_key = Config.SECRET_KEY

    register_routes(app)
    item_routes(app)

    return app

