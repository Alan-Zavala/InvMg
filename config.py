import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secretkey'
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False