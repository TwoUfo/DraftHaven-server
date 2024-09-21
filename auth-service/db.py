from flask import g, current_app
from flask_pymongo import PyMongo
from werkzeug.local import LocalProxy


mongo = PyMongo()

def init_app(app):
    mongo.init_app(app)  # Attach PyMongo to the Flask app

def get_db():
    # Use the initialized mongo instance
    if 'db' not in g:
        g.db = mongo.db
    return g.db

db = LocalProxy(get_db)


def add_user(username, email, password):
    user_doc = {'username': username, 'email': email, 'password': password}
    return db.users.insert_one(user_doc)


def find_user(username):
    user_doc = db.users.find_one({'username': username})
    return user_doc