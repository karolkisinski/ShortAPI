import unittest
import os
import json
from app import create_app, db


class ShortAPITestCase(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client
        self.urllist = {
            'title' : 'Test url',
            'url' : 'http://localhost.com/ogeg/dgeg/egdg'
            }
        
        with self.app.app_context():
            db.create_all()     

    def register_user(self, email="user@test.com", password="test123123"):
        """HELP FUNCTION register a test user"""
        user_data = {
            'email': email,
            'password': password
        }
        return self.client().post('/auth/register', data=user_data)

    def login_user(self, email="user@test.com", password="test123123"):
        """HELP FUNCTION login as test user"""
        user_data = {
            'email': email,
            'password': password
        }
        return self.client().post('/auth/login', data=user_data)

    def test_urllist_creation(self):
        """Test API can create a shorturl (POST request)"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        # create url by POST request
        res = self.client().post(
            '/urllist/', 
            headers=dict(Authorization="Bearer " + access_token),
            data=self.urllist
            )
        self.assertEqual(res.status_code, 201)
        self.assertIn('Test url', str(res.data))
    
    def test_api_can_get_all_urls(self):
        """Test API can get a shorturls (GET request)."""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        res = self.client().post(
        '/urllist/', 
        headers=dict(Authorization="Bearer " + access_token),
        data=self.urllist
        )
        self.assertEqual(res.status_code, 201)
        res = self.client().get('/urllist/')
        self.assertEqual(res.status_code, 200)
        self.assertIn('Test url', str(res.data))

    def test_api_can_get_url_by_id(self):
        """Test API can get a single shorturl by using it's id."""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        
        res = self.client().post(
        '/urllist/', 
        headers=dict(Authorization="Bearer " + access_token),
        data=self.urllist
        )
        self.assertEqual(res.status_code, 201)
        result_in_json = json.loads(res.data.decode('utf-8').replace("'", "\""))
        result = self.client().get(
            '/urllist/{}'.format(result_in_json['id']),
            headers=dict(Authorization="Bearer " + access_token)
            )
        self.assertEqual(result.status_code, 200)
        self.assertIn('Test url', str(result.data))

    def test_api_can_be_edited(self):
        """Test API can edit an existing shorturl. (PUT request)"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        res = self.client().post(
            '/urllist/{}'.format(results['id']),
            headers=dict(Authorization="Bearer " + access_token),
            data = {
                'title' : 'Test url 3',
                'url' : 'http://localhost.com/ogeg/dgeg/egdg'
            })
        self.assertEqual(res.status_code, 201)
        
        results = json.loads(res.data.decode())

        res = self.client().put(
            '/urllist/{}'.format(results['id']),
            headers=dict(Authorization="Bearer " + access_token),
            data = {
                'title' : 'Edit method worked'
            })
        self.assertEqual(res.status_code, 200)

        results = self.client().get(
            '/urllist/{}'.format(results['id']),
            headers=dict(Authorization="Bearer " + access_token),
            )
        self.assertIn('Edit method worked', results.data)

    def test_urllist_deletion(self):
        """Test API can delete an existing shorturl. (DELETE request)."""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        res = self.client().post(
            '/urllist/',
            headers=dict(Authorization="Bearer " + access_token),
            data = {
                'title' : 'Test url 4',
                'url' : 'http://localhost.com/ogeg/dgeg/egdg'
            })
        self.assertEqual(res.status_code,201)
        # get results in json
        results = json.loads(res.data.decode())

        res = self.client().delete(
                                    '/urllist/{}'.format(results['id']),
                                    headers=dict(Authorization="Bearer " + access_token)
                                  )
        self.assertEqual(res.status_code, 200)

        result = self.client().get(
                                    '/urllist/{}'.format(results['id']),
                                    headers=dict(Authorization="Bearer " + access_token)
                                  )
        self.assertEqual(result.status_code, 404)
    
    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
     
if __name__ == "__main__":
    unittest.main()