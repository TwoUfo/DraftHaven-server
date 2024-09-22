from flask_restx import Namespace, Resource
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, unset_jwt_cookies
from db import get_user_profile, create_new_draft, find_draft

api = Namespace('api', description='MAIN operations')

@api.route('/')
class Main(Resource):
    def get(self):
        pass

@api.route('/profile')
class Profile(Resource):
    @jwt_required()
    def get(self):
        user = get_jwt_identity()
        profile = get_user_profile(user)
        return profile
        

@api.route('/create-draft')
class Draft(Resource):
    @jwt_required()
    def get(self):
        pass
    
    @jwt_required()
    def post(self):
        user = get_jwt_identity()
        data = request.get_json()
        create_new_draft(data, user)
        

@api.route('/view/<title>')
class View(Resource):
    @jwt_required()
    def get(self, title):
        draft = find_draft(title)
        return jsonify(draft)
    


