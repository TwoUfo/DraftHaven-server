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

def create_new_draft(title, body, genre, user):
    author = user['username']
    draft_doc = {
        'title': title,
        'body': body,
        'genre': genre,
        'author': author
    }
    return db.drafts.insert_one(draft_doc)

def find_draft(title):
    draft_doc = db.drafts.find_one({'title': title}, {'_id': 0})
    return draft_doc

def get_drafts():
    drafts_doc = db.drafts.find({}, {'_id': 0})
    return list(drafts_doc)

def check_author(username, title):
    draft = find_draft(title)
    author = draft.get('author')
    
    if author != username:
        return None
    return author
    
def update_draft(title, n_title, n_body, n_genre, username):
    
    # ADD AUTHOR CHECK
     
    response = db.drafts.update_one(
        {'title': title}, 
        {'$set': {
            'title': n_title,
            'body': n_body,
            'genre': n_genre
        }})
    return response
    