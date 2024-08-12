from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from functools import wraps

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        current_user = get_jwt_identity()
        if current_user['role'] != "ADMINISTRADOR":
            return jsonify({'message': 'Admin role required'}), 403
        return fn(*args, **kwargs)
    return wrapper