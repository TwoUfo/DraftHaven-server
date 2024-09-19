from flask import Flask
from flask_restx import Api
from api.auth import api as auth_api

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')  

    api = Api(app)
    api.add_namespace(auth_api)

    return app