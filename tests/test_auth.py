import unittest
import json
from app import create_app, db

class AuthTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(config_name="testing")

        # initialize test client
        self.client = self.app.test_client

        # predefined json with user date
        self.user_date = {
            'email': 'test@example.com',
            'password': 'test_password123@'
        }

        with self.app.app_context():
            # create all tables
            db.session_close()
            db.drop_all()
            db.create_all()
        
        def test_registration(self):
            """Test user registration works correctly."""
            res = self.client().post('/auth/register', data=self.user_data)
            # get the results returned in json
            result = json.loads(res.data.decode())
            # assert that the request contains a success message and a 201 SC
            self.assertEqual(result['message'], "You registered successfully.")
            self.assertEqual(res.status_code, 201)

        def test_already_registered_user(self):
            """Test that a user cannot be registered twice."""
            res = self.client().post('/auth/register', data=self.user_data)
            self.assertEqual(res.status_code, 201)
            second_res = self.client().post('/auth/register', data=self.user_data)
            self.assertEqual(second_res.status_code, 202)
            # get the results returned in json format
            result = json.loads(second_res.data.decode())
            self.assertEqual(
                result['message'], "User already exists. Please login.")