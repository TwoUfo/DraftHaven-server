import os

class Config:
    MONGO_URI = 'mongodb://auth-db:27017/authdb'
    
    JWT_SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret')
    JWT_TOKEN_LOCATION = ['cookies']
    JWT_COOKIE_SECURE = False
    JWT_ACCESS_COOKIE_NAME = 'access_token_cookie'
    JWT_COOKIE_CSRF_PROTECT = False

