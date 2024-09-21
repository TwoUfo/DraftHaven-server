from flask_restx import Namespace, Resource
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, unset_jwt_cookies
from db import get_user_profile

api = Namespace('api', description='MAIN operations')

@api.route('/profile')
class Profile(Resource):
    @jwt_required()
    def get(self):
        user = get_jwt_identity()
        profile = get_user_profile(user)
        return profile
        
        