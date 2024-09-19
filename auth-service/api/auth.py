from flask_restx import Namespace, Resource
from flask import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, unset_jwt_cookies
from .auth_utils import hash_password, check_password
from db import add_user, find_user

api = Namespace('api', description='API operations')

@api.route('/registration')
class Register(Resource):
    def post(self):
        data = request.get_json()
        username = data['username']
        email = data['email']
        hashed_password = hash_password(data['password'])
        
        # Додаємо нового користувача
        add_user(username, email, hashed_password)
        
        return {'message': 'User registered successfully'}, 201
    

@api.route('/login')
class Login(Resource):
    def post(self):
        data = request.get_json()
        username = data['username']
        password = data['password']
        
        document = find_user(username)
        
        if not document or not check_password(document['password'], password):
            return {'message': 'Incorrect username or password'}, 401
        
        access_token = create_access_token(identity=username)
        response = jsonify({'message': 'Logged in'})
        response.set_cookie('access_token_cookie', access_token, httponly=True)
        
        return response
            
@api.route('/logout')
class Logout(Resource):
    @jwt_required()
    def post(self):
        response = jsonify({'message': 'Logged out'})
        unset_jwt_cookies(response)
        return response
