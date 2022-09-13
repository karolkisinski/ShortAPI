import unittest
import os
import json
from app import create_app, db


class ShortAPITestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client
        self.urllist = {
            'title' : 'Test url',
            'url' : 'http://localhost.com/ogeg/dgeg/egdg',
            'short_url' : 'http://short.com/abcd'
            }
        
        with self.app.app_context():
            db.create_all()
        

    def test_urllist_creation(self):
        res = self.client().post('/urllist/', data=self.urllist)
        self.assertEqual(res.status_code, 201)
        self.assertIn('Test url', str(res.data))
        print(str(res.data))
    
    def test_api_can_get_all_urls(self):
        res = self.client().post('/urllist/', data=self.urllist)
        self.assertEqual(res.status_code, 201)
        res = self.client().get('/urllist/')
        self.assertEqual(res.status_code, 200)
        self.assertIn('Test url', str(res.data))
        print(str(res.data))
        
if __name__ == "__main__":
    unittest.main()