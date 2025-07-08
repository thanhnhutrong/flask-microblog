from flask import Flask

def create_app():
    app = Flask(__name__)

    # dang ky cac route tu route.py
    from .routes import main
    app.register_blueprint(main)

    return app