from flask_restx import Namespace, Resource
from flask import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, unset_jwt_cookies
from .auth_utils import hash_password, check_password

api = Namespace('api', description='API operations')