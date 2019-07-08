import os
from dotenv import load_dotenv
load_dotenv()

class Config(object):
    SECRET_KEY = os.environ['SECRET_KEY'] or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SQLALCHEMY_TRACK_MODIFICATIONS = False

