import base64
from functools import wraps

from config import Config
from flask import jsonify, request


def require_admin_login(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        basic_auth_header = request.headers.get('Authorization')
        if basic_auth_header is None:
            return jsonify({
                        'msg': "header 'Authorization' is required",
                    }), 401

        auth_header = basic_auth_header[6:]
        admin, pwd = base64.b64decode(auth_header).decode().split(':')
        if admin == Config.ADMIN and pwd == Config.ADMINPWD:
                return func(*args, **kwargs)
        else:
            return jsonify({
                    'msg': 'Authorization failed',
                }), 401
    return wrapper
