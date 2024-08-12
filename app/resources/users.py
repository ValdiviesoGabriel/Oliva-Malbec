from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app import db
from app.models.user import User
from app.models.user_data import UserData
from app.models.role import Role
from app.models.profile import Profile
from app.services.fetchers import *
from app.utils.role_required import admin_required
from app.utils.security import check_password, set_password

user_bp = Blueprint("user", __name__)

@user_bp.route("/users", methods = ["POST"])
@jwt_required()
@admin_required
def create_user():
    try:
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")
        role_name = data.get("role")
        if role_name == None:
            role_name = "ESTUDIANTE"
        
        #Validations
        if not email or not password:
            return jsonify({"message": "Email and password are required"}), 400
        
        if User.query.filter_by(email = email).first():
            return jsonify({"message": "Email already registered"}), 400
        
        role = Role.query.filter_by(name = role_name).first()

        #User Data creation for User
        user_data = UserData(
            first_name = None,
            last_name = None,
            dni = None,
            phone = None,
            address = None,
        )
        db.session.add(user_data)
        db.session.commit()
        
        #User creation
        user = User(email = email, userdata = user_data)
        user.password_hash = (set_password(password))
        db.session.add(user)
        db.session.commit()
        
        #Profile creation for User
        profile = Profile(user_id = user.id, role_id = role.id)
        db.session.add(profile)
        db.session.commit()
        
        return jsonify({"message": "User registered successfully", "id": user.id}), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 404

@user_bp.route("/users", methods = ["GET"])
@jwt_required()
@admin_required
def get_all_users():
    users = User.query.all()
    users_list = []
    for user in users:
        data = {
            "id" : user.id,
            "email" : user.email,
            "first_name" : user.userdata.first_name,
            "last_name" : user.userdata.last_name
        }
        users_list.append(data)
    return jsonify({"users": users_list}), 200

@user_bp.route("/users/<int:user_id>", methods = ["GET"])
@jwt_required()
@admin_required
def get_user_by_id(user_id):
    try:
        user = fetch_user(user_id)
        
        data = {
            "id" : user.id,
            "email" : user.email,
            "first_name" : user.userdata.first_name,
            "last_name" : user.userdata.last_name
        }
        return jsonify({"user": data}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 404
    
@user_bp.route("/users/<int:user_id>", methods = ["PUT"])
@jwt_required()
@admin_required
def update_user(user_id):
    try:
        user = fetch_user(user_id)
        
        data = request.get_json()
        
        if 'email' in data:
                user.email = data['email']
        if 'password' in data:
            user.set_password(data['password'])
        if 'dni' in data:
            user.userdata.dni = data['dni']
        if 'first_name' in data:
            user.userdata.first_name = data['first_name']
        if 'last_name' in data:
            user.userdata.last_name = data['last_name']
        if 'address' in data:
            user.userdata.address = data['address']
        if 'phone' in data:
            user.userdata.phone = data['phone']
        
        db.session.commit()
        return jsonify({"message": "User updated successfully"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 404

@user_bp.route("/users/<int:user_id>", methods = ["DELETE"])
@jwt_required()
@admin_required
def delete_user(user_id):
    try:
        user = User.query.filter_by(id = user_id).first()
        
        if not user:
            return jsonify({"message": "User not found"}), 400
        
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted successfully"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 404