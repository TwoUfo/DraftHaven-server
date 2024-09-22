from flask import g, current_app
from flask_pymongo import PyMongo
from werkzeug.local import LocalProxy


mongo = PyMongo()

def init_db(app):
    mongo.init_app(app)  

def get_db():
    if 'db' not in g:
        g.db = mongo.db
    return g.db

db = LocalProxy(get_db)


def add_user(username, email, password):
    existing_user = db.users.find_one({'$or': [{'username': username}, {'email': email}]})
    
    if existing_user:
        return "User with this username or email already exists", 409
    
    user_doc = {'username': username, 'email': email, 'password': password}
    db.users.insert_one(user_doc)
    return {'message': 'User registered successfully'}, 201


def find_user(username):
    user_doc = db.users.find_one({'username': username})
    return user_doc
