import unittest
import os
from app import db, create_app
from app.models.role import Role

class TestRoleModel(unittest.TestCase):
    
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
        
    def test_role_creation(self):
        role = Role(name = "TEST")
        db.session.add(role)
        db.session.commit()
        
        fetched_role = Role.query.filter_by(name = "TEST").first()
        self.assertIsNotNone(fetched_role)
        self.assertEqual(fetched_role.name, "TEST")
        
if __name__ == "__main__":
    unittest.main()