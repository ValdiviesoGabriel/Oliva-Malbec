import unittest
import os
from sqlalchemy import text
from app import create_app, db

class ConnectionTestCase(unittest.TestCase):
    
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
    
    def test_db_connection(self):
        result = db.session.query(text("'Testing'")).one()
        self.assertEqual(result[0], "Testing")

if __name__ == "__main__":
    unittest.main()