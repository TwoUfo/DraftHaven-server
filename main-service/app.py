from flask import Flask
from flask_restx import Api
from flask_jwt_extended import JWTManager
from api.main import api as main_api
from db import init_db
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    init_db(app)
    
    jwt = JWTManager()  
    jwt.init_app(app)

    api = Api(app)
    api.add_namespace(main_api)

    CORS(app, supports_credentials=True)

    return app