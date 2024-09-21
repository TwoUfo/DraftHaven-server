from flask_restx import Namespace, Resource
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, unset_jwt_cookies

api = Namespace('api', description='MAIN operations')

@api.route('/profile')
class Profile(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        return jsonify({'user': current_user})