import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-please-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # LINE Login設定
    LINE_CHANNEL_ID = os.environ.get('LINE_CHANNEL_ID')
    LINE_CHANNEL_SECRET = os.environ.get('LINE_CHANNEL_SECRET')
    LINE_CALLBACK_URL = os.environ.get('LINE_CALLBACK_URL', 'http://localhost:5000/auth/line/callback') 