import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'bca_cms_secret_key_2026_987654321'
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'instance', 'database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
