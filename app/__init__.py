from flask import Flask # create object Flask from package Flask
from config import Config

app = Flask(__name__) # variables predefine
app.config.from_object(Config)

from app import routes # import package routes, nen import o cuoi vi can app variable
