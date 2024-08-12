import unittest
import os
from flask_jwt_extended import create_access_token
from app import db, create_app
from app.models.course import Course
from app.models.course_user import CourseUser
from app.models.profile import Profile
from app.models.role import Role
from app.utils.initializers import initialize_roles
from app.services.fetchers import *
from app.utils.security import set_password

class TestCourseBP(unittest.TestCase):
    
    def setUp(self):
        os.environ["FLASK_CONTEXT"] = "testing"
        self.app = create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        
        initialize_roles()
        
        #ADMIN USER
        self.user = User(email = "admin@test.com", userdata = UserData())
        self.user.password_hash = set_password("admin")
        role = Role.query.filter_by(name = "ADMINISTRADOR").first()
        self.profile = Profile(user_id = self.user.id, role_id = role.id)
        
        db.session.add(self.user)
        db.session.add(self.profile)
        db.session.commit()
        
        self.token = create_access_token(identity = {"id": self.user.id, "role" : role.name})
        
    def tearDown(self):
        db.session.rollback()
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_create_course(self):
        data = {
            "name": "test"
        }
        
        response = self.client.post("/courses", json = data, headers = {"Authorization": f"Bearer {self.token}"})
        
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.json)
        self.assertEqual(response.json["message"], "Course registered successfully")
        
        created_course_id = response.json["id"]
        created_course = fetch_course(created_course_id)
        
        self.assertIsNotNone(created_course)
        self.assertEqual(created_course.name, "test")
        self.assertEqual(created_course.id, created_course_id)
        
    def test_get_all_courses(self):
        course1 = Course(name = "course1")
        course2 = Course(name = "course2")
        db.session.add(course1)
        db.session.add(course2)
        db.session.commit()
        
        response = self.client.get("/courses", headers = {"Authorization": f"Bearer {self.token}"})
        
        self.assertEqual(response.status_code, 200)
        courses = response.json["courses"]
        
        self.assertIsNotNone(courses)
        
        courses_names = [course["name"] for course in courses]
        self.assertIn("course1", courses_names)
        self.assertIn("course2", courses_names)
    
    def test_get_course_by_id(self):
        course = Course(name = "test")
        db.session.add(course)
        db.session.commit()
        
        course_id = course.id
        response = self.client.get(f"/courses/{course_id}", headers = {"Authorization": f"Bearer {self.token}"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["course"]["id"], course_id)
        self.assertEqual(response.json["course"]["name"], "test")
    
    def test_update_course(self):
        course = Course(name = "test")
        db.session.add(course)
        db.session.commit()
        
        data = {
            "name": "updated"
        }
        course_id = course.id
        response = self.client.put(f"/courses/{course_id}", json = data, headers = {"Authorization": f"Bearer {self.token}"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["message"], "Course updated successfully"), 200
        
        course_updated = fetch_course(course_id)
        self.assertIsNotNone(course_updated)
        self.assertEqual(course_updated.name, "updated")
        
    def test_delete_course(self):
        course = Course(name = "test")
        db.session.add(course)
        db.session.commit()
        
        course_id = course.id
        response = self.client.delete(f"/courses/{course_id}", headers = {"Authorization": f"Bearer {self.token}"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["message"], "Course deleted successfully"), 200
        
    def enroll_user(self):
        course = Course(name = "test")
        user = User(email = "test@test.com")
        db.session.add(course)
        db.session.add(user)
        db.session.commit()
        
        data = {
            "user_id": user.id,
            "course_id": course.id,
            "grade": "8"
        }
        
        response = self.client.post(f"/courses/enroll", json = data, headers = {"Authorization": f"Bearer {self.token}"})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json["message"], "User enrolled successfully")
        
        user_enrolled = fetch_course_user(user_id = user.id, course_id = course.id)
        self.assertIsNotNone(user_enrolled)
    
    def get_users_by_course(self):
        course = Course(name = "test")
        user = User(email = "test@test.com")
        db.session.add(course)
        db.session.add(user)
        db.session.commit()
        
        course_user = CourseUser(user_id = user.id, course_id = course.id, grade = "5")
        db.session.add(course_user)
        db.session.commit()
        
        response = self.client.get(f"/courses/{course.id}/users", headers = {"Authorization": f"Bearer {self.token}"})
        
        self.assertEqual(response.status_code, 200)
        self.assertIn("users", response.json)
        
if __name__ == "__main__":
    unittest.main()