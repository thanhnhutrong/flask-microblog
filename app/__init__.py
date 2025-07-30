from flask import Flask # create object Flask from package Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os

app = Flask(__name__) # variables predefine
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

if not app.debug:
    if app.config['MAIL_SERVER']:
        print('Hello')
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost = (app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            # fromaddr='no-reply@' + app.config['MAIL_SERVER'],
            fromaddr=app.config['VERIFYEMAIL'],
            toaddrs=app.config['ADMINS'], subject='Microblog Failure',
            credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240, backupCount=10) # thiet lap, moi ban ghi se la 10k byte, neu vuot qua se ghi sang ban khac, khong qua 10 ban
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')) # thiet lap format de log de doc hon: thoi gian, message, level, file va so dong sinh ra log
    file_handler.setLevel(logging.INFO) # chi ghi nhung log o muc do INFO tro len (INFO, WARNING, ERROR, CRITICAL)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO) # cho phep log o muc do INFO tro len tren toan bo log cua flask app
    app.logger.info('Microblog startup') # ghi vao dau log

from app import routes, models, errors # import package routes, nen import o cuoi vi can app variable