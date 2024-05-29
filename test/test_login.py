import unittest
from app import create_app, db
from app.models.user import User

class LoginTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

        #Test User
        user = User(username = "testuser", email = "testuser@test.com")
        user.set_password("testuserpassword")
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_login_success(self):
        resp = self.client.post("/api/login", json = {
            "username" : "testuser",
            "password" : "testuserpassword"
        })
        self.assertEqual(resp.status_code, 200)
        self.assertIn("Login sucessful", resp.get_json()["message"])

    def test_login_failure(self):
        resp = self.client.post("/api/login", json = {
            "username" : "testuser",
            "password" : "testuserpasswordfail"
        })
        self.assertEqual(resp.status_code, 401)
        self.assertIn("Failed login", resp.get_json()["message"])

if __name__ == "__main__":
    unittest.main()