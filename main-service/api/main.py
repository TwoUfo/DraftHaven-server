from flask_restx import Namespace, Resource
from flask import request, jsonify, redirect
from flask_jwt_extended import jwt_required, get_jwt_identity, unset_jwt_cookies
from db import get_user_profile, create_new_draft, find_draft, get_drafts, update_draft


api = Namespace('api', description='MAIN operations')

@api.route('/')
class Main(Resource):
    def get(self):
        drafts = get_drafts()
        return jsonify(drafts)

@api.route('/profile')
class Profile(Resource):
    @jwt_required()
    def get(self):
        user = get_jwt_identity()
        profile = get_user_profile(user)
        return profile
        

@api.route('/drafts/create')
class Create(Resource):
    @jwt_required()
    def get(self):
        pass
    
    @jwt_required()
    def post(self):
        user = get_jwt_identity()
        data = request.get_json()
        create_new_draft(data, user)
        return redirect(f"http://127.0.0.1:5002/api/view/{data['title']}", 302)


@api.route('/drafts/update/<title>')
class Update(Resource):
    def put(self, title):
        data = request.get_json()
        update_draft(title, data)
        return {"message": "Draft updated successfully"}, 200
    

@api.route('/drafts/view/<title>')
class View(Resource):
    @jwt_required()
    def get(self, title):
        draft = find_draft(title)
        return jsonify(draft)

