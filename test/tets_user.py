import unittest
from app import create_app, db
from app.models.user import User

class TestUserModel(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        user = User(username = "testuser", email = "test@test.com")
        user.set_password("password123")
        self.assertFalse(user.check_password("password1234"))
        self.assertTrue(user.check_password("password123"))

    def test_create_admin_user(self):
        admin = User(username = "testadmin", email = "testadmin@test.com", is_admin = True)
        admin.set_password("adminpassword")
        db.session.add(admin)
        db.session.commit()
        self.assertTrue(admin.is_admin)

    def test_create_student_user(self):
        student = User(username = "studenttest", email = "teststudent@test.com", is_admin = False)
        student.set_password("studentpassword")
        db.session.add(student)
        db.session.commit()
        self.assertFalse(student.is_admin)

if __name__ == "__main__":
    unittest.main()