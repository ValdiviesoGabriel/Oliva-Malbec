import unittest
import os
from app import db, create_app
from app.models.course_user import CourseUser
from app.models.course import Course
from app.models.user import User
from app.utils.security import set_password

class TestCourseUserModel(unittest.TestCase):
    
    def setUp(self):
        os.environ["FLASK_CONTEXT"] = "testing"
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
    
    def tearDown(self):
        db.session.rollback()
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        
    def test_course_user(self):
        user = User(email = "test@test.com")
        user.password_hash = set_password("test")
        course = Course(name = "test-course")
        db.session.add(user)
        db.session.add(course)
        db.session.commit()
        
        course_user = CourseUser(user_id = user.id, course_id = course.id, grade = "50")
        db.session.add(course_user)
        db.session.commit()
        
        fetched_course_user = CourseUser.query.filter_by(course_id = course.id).first()
        self.assertIsNotNone(fetched_course_user)
        self.assertEqual(fetched_course_user.course_id, course.id)
        self.assertEqual(fetched_course_user.user_id, user.id)
        self.assertEqual(fetched_course_user.grade, "50")
        
if __name__ == "__main__":
    unittest.main()