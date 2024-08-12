from flask import jsonify
from app.models.course import Course
from app.models.course_user import CourseUser
from app.models.user import User
from app.models.user_data import UserData

def fetch_course(course_id):
    course = Course.query.filter_by(id=course_id).first()
    if not course:
        raise Exception('Course not found')
    return course

def fetch_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        raise Exception('User not found')
    return user

def fetch_user_by_email(email):
    user = User.query.filter_by(email = email).first()
    if not user:
        raise Exception("User not found")
    return user

def fetch_user_data(user_id):
    user_data = UserData.query.filter_by(user_id=user_id).first()
    return user_data

def fetch_course_user(user_id, course_id):
    course_user = CourseUser.query.filter_by(user_id = user_id, course_id = course_id).first()
    if course_user:
        raise Exception("User already enrolled.")
    