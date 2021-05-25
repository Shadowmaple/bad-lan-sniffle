from flask import Blueprint

api = Blueprint('api', __name__)

from . import article, dictionary, library, sniffle, sniffle2
