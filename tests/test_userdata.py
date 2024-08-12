import unittest
import os
from app import create_app, db
from app.models.user_data import UserData

class TestUserDataModel(unittest.TestCase):
    
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
    
    def test_userdata_creation(self):
        userdata = UserData(first_name = "test", last_name = "test2", dni = "1234", phone = "123456", address = "123 test")
        self.assertEqual(userdata.first_name, "test")
        self.assertEqual(userdata.last_name, "test2")
        self.assertEqual(userdata.dni, "1234")
        self.assertEqual(userdata.phone, "123456")
        self.assertEqual(userdata.address, "123 test")

if __name__ == "__main__":
    unittest.main()