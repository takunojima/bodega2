import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # LINE Login configuration
    LINE_CHANNEL_ID = os.environ.get('LINE_CHANNEL_ID')
    LINE_CHANNEL_SECRET = os.environ.get('LINE_CHANNEL_SECRET')
    
    # Production configuration
    SERVER_NAME = os.environ.get('SERVER_NAME', 'bodegashift.com')
    PREFERRED_URL_SCHEME = os.environ.get('PREFERRED_URL_SCHEME', 'http')
    SESSION_COOKIE_SECURE = False
    REMEMBER_COOKIE_SECURE = False
    SESSION_COOKIE_DOMAIN = '.bodegashift.com'
    
    # Security headers
    STRICT_TRANSPORT_SECURITY = False
    STRICT_TRANSPORT_SECURITY_PRELOAD = False
    STRICT_TRANSPORT_SECURITY_MAX_AGE = 0
    STRICT_TRANSPORT_SECURITY_INCLUDE_SUBDOMAINS = False

    # LINE Login callback
    LINE_CALLBACK_URL = os.environ.get('LINE_CALLBACK_URL', 'http://bodegashift.com/auth/line/callback') 