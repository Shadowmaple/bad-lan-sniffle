from flask import Blueprint

api = Blueprint('api', __name__)

# from . import login, courses, assign, user, notice, search
# from . import email, notice_config
from . import create, list, update
