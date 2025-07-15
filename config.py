import os
basedir = os.path.abspath(os.path.dirname(__file__)) # lay duong dan toi file ma nguon hien tai -> ching la folder to-do-list-flask

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
