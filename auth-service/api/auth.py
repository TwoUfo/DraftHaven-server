from flask_restx import Namespace, Resource
from flask import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, unset_jwt_cookies
from .auth_utils import hash_password, check_password
from .utils import expect
from db import add_user, find_user

api = Namespace('api', title='auth API')

@api.route('/registration')
class Register(Resource):
    def post(self):
        data = request.get_json()
        try:
            password_1 = expect(data.get('first-password'), str, 'first-password')
            password_2 = expect(data.get('second-password'), str, 'second-password')
            if password_1 != password_2:
                return {'mismatch': 'passwords do not match'}, 401          
            
            username = expect(data.get('username'), str, 'username')
            email = expect(data.get('email'), str, 'email')
            
            hashed_password = hash_password(password_1)
            
            response, status_code = add_user(username, email, hashed_password)

            return response, status_code
        except Exception as e:
            return jsonify({'error': str(e)}), 400
    

@api.route('/login')
class Login(Resource):
    def post(self):
        data = request.get_json()
        try:
            username = expect(data.get('username'), str, 'username')
            password = expect(data.get('password'), str, 'password')
            
            document = find_user(username)
            
            if not document or not check_password(document['password'], password):
                return {'message': 'Incorrect username or password'}, 401
            
            access_token = create_access_token(identity={'username': username, 'email': document['email']})
            response = jsonify({'message': 'Logged in'})
            response.set_cookie('access_token_cookie', access_token, httponly=True)
            return response
        except Exception as e:
            return jsonify({'error': str(e)}), 400
        
        
@api.route('/logout')
class Logout(Resource):
    @jwt_required()
    def post(self):
        try:
            response = jsonify({'message': 'Logged out'})
            unset_jwt_cookies(response)
            return response
        except Exception as e:
            return jsonify({'error': str(e)}), 400
