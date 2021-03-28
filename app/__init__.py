from config import Config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

from .api import api as api_app

app.register_blueprint(api_app, url_prefix="/api/v1")
