import os
from dotenv import load_dotenv
load_dotenv()

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI ='postgresql://localhost/trhs'
    SQLALCHEMY_TRACK_MODIFICATIONS = False