from flask import g, current_app
from flask_pymongo import PyMongo
from werkzeug.local import LocalProxy


def get_db():
    db = getattr(g, "_database", None)

    if db is None:
        db = g._database = PyMongo(current_app).db

    return db

db = LocalProxy(get_db)


def add_user(username, email, password):
    user_doc = {'username': username, 'email': email, 'password': password}
    return db.users.insert_one(user_doc)


def find_user(username):
    user_doc = db.users.find_one({'username': username})
    return user_doc