from flask_restx import Namespace, Resource
from flask import request, jsonify, redirect
from flask_jwt_extended import jwt_required, get_jwt_identity, unset_jwt_cookies
from db import get_user_profile, create_new_draft, find_draft, get_drafts, update_draft, check_author
from .utils import expect


api = Namespace('api', description='MAIN operations')

@api.route('/')
class Main(Resource):
    def get(self):
        try:
            drafts = get_drafts()
            return jsonify(drafts)
        except Exception as e:
            return jsonify({'error': str(e)}), 400


@api.route('/profile')
class Profile(Resource):
    @jwt_required()
    def get(self):
        try:
            user = get_jwt_identity()
            profile = get_user_profile(user)
            return profile
        except Exception as e:
            return jsonify({'error': str(e)}), 400
        
    @jwt_required()
    def put(self):
        try:
            #UPDATE USER DATA
            
            pass
        except Exception as e:
            return jsonify({'error': str(e)}), 400
        

@api.route('/drafts')
class Drafts(Resource):
    def get(self):
        try:
            drafts = get_drafts()
            return drafts
        except Exception as e:
                return jsonify({'error': str(e)}), 400

@api.route('/drafts/create')
class Create(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()
        try:
            title = expect(data.get('title'), str, 'title')
            body = expect(data.get('body'), str, 'body')
            genre = expect(data.get('genre'), str, 'genre')
            
            user = get_jwt_identity()
            new_draft = create_new_draft(title, body, genre, user)
            if new_draft:
                return redirect(f"http://127.0.0.1:5002/api/drafts/view/{data['title']}", 302)
        except Exception as e:
            return jsonify({'error': str(e)}), 400


@api.route('/drafts/update/<title>')
class Update(Resource):
    @jwt_required()
    def get(self, title):
        try:
            user = get_jwt_identity()
            if not check_author(title, user['username']):
                return redirect(f"http://127.0.0.1:5002/api/drafts/view/{title}", 302)
        except Exception as e:
            return jsonify({'error': str(e)}), 400
        
    @jwt_required()
    def put(self, title):
        data = request.get_json()
        try:
            user = get_jwt_identity()
            
            n_title = expect(data.get('title'), str, 'title')
            n_body = expect(data.get('body'), str, 'body')
            n_genre = expect(data.get('genre'), str, 'genre')
            
            update_draft(title, n_title, n_body, n_genre, user['username'])
            return {"message": "Draft updated successfully"}, 200
        except Exception as e:
                return jsonify({'error': str(e)}), 400


@api.route('/drafts/view/<title>')
class View(Resource):
    @jwt_required()
    def get(self, title):
        try:
            draft = find_draft(title)
            return jsonify(draft)
        except Exception as e:
            return jsonify({'error': str(e)}), 400
