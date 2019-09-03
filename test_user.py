import json
import unittest

from app import create_app, db

# headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}


class UserTestCase(unittest.TestCase):
    """This class represents the users test case"""

    def setUp(self):
        """Define test variables and initialize app"""
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.user = {'username': 'Administrator', 'password': 'Password_of_Administrator'}

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_user_creation(self):
        """Test API can create a user (POST request)"""
        res = self.client.post('/users/', data=self.user)
        self.assertEqual(res.status_code, 201)
        res = self.client.get('/users/')
        self.assertEqual(res.status_code, 200)
        self.assertIn('Administrator', str(res.data))

    def test_api_can_get_user_by_id(self):
        """Test API can get a single user by using it's id"""
        rv = self.client.post('/users/', data=self.user)
        self.assertEqual(rv.status_code, 201)
        result_in_json = json.loads(rv.data.decode('utf-8').replace("'", "\""))
        result = self.client.get(f'/users/{result_in_json["id"]}')
        self.assertEqual(result.status_code, 200)
        self.assertIn('Administrator', str(result.data))

    def test_user_can_be_edit(self):
        """Test API can edit an existing user (PUT request)"""
        rv = self.client.post('/users/', data={'username': 'Businessman', 'password': 'Password_of_Businessman'})
        self.assertEqual(rv.status_code, 201)
        rv = self.client.put('/users/1', data={'username': 'Employee', 'password': 'Password_of_Employee'})
        self.assertEqual(rv.status_code, 200)
        results = self.client.get('/users/1')
        self.assertIn('Employee', str(results.data))

    def test_user_deletion(self):
        """Test API can delete an existing user (DELETE request)"""
        rv = self.client.post('/users/', data={'name': 'Businessman', 'password': 'Password_of_Businessman'})
        self.assertEqual(rv.status_code, 201)
        res = self.client.delete('/users/1')
        self.assertEqual(res.status_code, 200)
        # Test to see if it exists, should return a 404
        result = self.client.get('/users/1')
        self.assertEqual(result.status_code, 404)

    def tearDown(self):
        """teardown all initialized variables"""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()


# Make the unittest conveniently executable
if __name__ == '__main__':
    unittest.main()
