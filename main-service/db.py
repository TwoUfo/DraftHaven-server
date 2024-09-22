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

def get_user_profile(user):
    username = user['username']
    profile_doc = db.profiles.find_one({'username': username}, {'_id': 0}) 
    
    if profile_doc:
        return profile_doc
    else:
        db.profiles.insert_one(user)
        return user

def create_new_draft(draft_doc, user):
    author = user['username']
    draft_doc['author'] = author
    return db.drafts.insert_one(draft_doc)

def find_draft(title):
    draft_doc = db.drafts.find_one({'title': title}, {'_id': 0})
    return draft_doc