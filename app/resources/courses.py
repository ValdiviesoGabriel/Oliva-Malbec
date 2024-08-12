from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app import db
from app.models.course import Course 
from app.services.fetchers import *
from app.utils.role_required import admin_required

course_bp = Blueprint("course", __name__)

@course_bp.route("/courses", methods = ["POST"])
@jwt_required()
@admin_required
def create_course():
    try:
        data = request.get_json()
        name = data.get("name")
        
        if not name:
            return jsonify({"message": "Course name is required"}), 400
        
        if Course.query.filter_by(name = name).first():
            return jsonify({"message": "Course already registered"}), 400
        
        course = Course(name = name)
        db.session.add(course)
        db.session.commit()
        return jsonify({"message": "Course registered successfully", "id": course.id}), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 404
    
@course_bp.route("/courses", methods = ["GET"])
@jwt_required()
def get_all_courses():
    try:
        courses = Course.query.all()
        courses_list = []
        for course in courses:
            data = {
                "id" : course.id,
                "name" : course.name
            }
            courses_list.append(data)
        return jsonify({"courses": courses_list}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 404

@course_bp.route("/courses/<int:course_id>", methods = ["GET"])
@jwt_required()
def get_course_by_id(course_id):
    try:
        course = fetch_course(course_id)
        
        data = {
            "id" : course.id,
            "name" : course.name
        }
        return jsonify({"course": data}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 404
    
@course_bp.route("/courses/<int:course_id>", methods = ["PUT"])
@jwt_required()
@admin_required
def update_course(course_id):
    try:
        course = fetch_course(course_id)
        
        data = request.get_json()
        
        course.name = data["name"]
        
        db.session.commit()
        return jsonify({"message": "Course updated successfully"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 404

@course_bp.route("/courses/<int:course_id>", methods = ["DELETE"])
@jwt_required()
@admin_required
def delete_course(course_id):
    try:
        course = Course.query.filter_by(id = course_id).first()
        
        if not course:
            return jsonify({"message": "Course not found"}), 400
        
        db.session.delete(course)
        db.session.commit()
        return jsonify({"message": "Course deleted successfully"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 404

@course_bp.route("/courses/enroll", methods = ["POST"])
@jwt_required()
@admin_required
def enroll_user():
    try:
        data = request.get_json()
        
        user_id = data["user_id"]
        course_id = data["course_id"]
        grade = data.get("grade")
        
        fetch_user(user_id)
        fetch_course(course_id)
        fetch_course_user(user_id = user_id, course_id = course_id)
        
        course_user = CourseUser(user_id = user_id, course_id= course_id, grade = grade)
        db.session.add(course_user)
        db.session.commit()
        return jsonify({"message": "User enrolled successfully"}), 201
    
    #Exception for required camps -> user_id and course_id
    except KeyError as e:
        return jsonify({"message": f"{str(e)} is required"}), 400
    
    except Exception as e:
        return jsonify({"message": str(e)}), 404
    
@course_bp.route("/courses/<int:course_id>/users", methods = ["GET"])
@jwt_required()
@admin_required
def get_users_by_course(course_id):
    try:
        fetch_course(course_id)
        courses_users = CourseUser.query.filter_by(course_id = course_id).all()
        users_list = []
        for course_user  in courses_users:
            user = course_user.user
            data = {
                "id" : user.id,
                "email" : user.email,
                "dni" : user.userdata.dni,
                "first_name" : user.userdata.first_name,
                "last_name" : user.userdata.last_name,
                "grade" : course_user.grade
            }
            users_list.append(data)
        return jsonify({"users": users_list}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 404