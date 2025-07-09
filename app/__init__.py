from flask import Flask
from flask_sqlalchemy import SQLAlchemy

def create_app():
    app = Flask(__name__)

    # dang ky cac route tu route.py
    from .routes import main
    app.register_blueprint(main)

    return app

# app = Flask(__name__)
# ## /// = relative path, //// = absolute path
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.lite'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)