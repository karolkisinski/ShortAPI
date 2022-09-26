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
            'url' : 'http://localhost.com/ogeg/dgeg/egdg'
            }
        
        with self.app.app_context():
            db.create_all()     

    def test_urllist_creation(self):
        res = self.client().post('/urllist/', data=self.urllist)
        self.assertEqual(res.status_code, 201)
        self.assertIn('Test url', str(res.data))
    
    def test_api_can_get_all_urls(self):
        res = self.client().post('/urllist/', data=self.urllist)
        self.assertEqual(res.status_code, 201)
        res = self.client().get('/urllist/')
        self.assertEqual(res.status_code, 200)
        self.assertIn('Test url', str(res.data))

    def test_api_can_get_url_by_id(self):
        res = self.client().post('/urllist/', data=self.urllist)
        self.assertEqual(res.status_code, 201)
        result_in_json = json.loads(res.data.decode('utf-8').replace("'", "\""))
        result = self.client().get(
            '/urllist/{}'.format(result_in_json['id']))
        self.assertEqual(result.status_code, 200)
        self.assertIn('Test url', str(result.data))

    def test_api_can_be_edited(self):
        res = self.client().post(
            '/urllist/',
            data = {
                'id': 1,
                'title' : 'Test url 3',
                'url' : 'http://localhost.com/ogeg/dgeg/egdg'
            })
        self.assertEqual(res.status_code, 201)
        res = self.client().put(
            '/urllist/1',
            data = {
                'title' : 'Test url 3 changed'
            })
        self.assertEqual(res.status_code, 200)
        results = self.client().get('/urllist/1')
        self.assertIn('Test url 3 changed', str(results.data))

    def test_urllist_deletion(self):
        res = self.client().post(
            '/urllist/',
            data = {
                'title' : 'Test url 4',
                'url' : 'http://localhost.com/ogeg/dgeg/egdg'
            })
        self.assertEqual(res.status_code,201)
        res = self.client().delete('/urllist/1')
        self.assertEqual(res.status_code, 200)
        result = self.client().get('/urllist/1')
        self.assertEqual(result.status_code, 404)
    
    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
     
if __name__ == "__main__":
    unittest.main()