import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie

# set token for different roles
assistant_token = os.environ['assistant_token']
director_token = os.environ['director_token']
producer_token = os.environ['producer_token']
# set auth header for different roles
def auth_header(role):
    if role == 'assistant':
        return {'Authorization': 'Bearer {}'.format(assistant_token)}
    elif role == 'director':
        return {'Authorization': 'Bearer {}'.format(director_token)}
    elif role == 'producer':
        return {'Authorization': 'Bearer {}'.format(producer_token)}

class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the casting agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "casting_agency_test"
        self.database_path = "postgres://{}:{}@{}/{}".format('postgres','postgres','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # sample actor to use in some test cases
        self.new_actor = {
            'name': 'Leonardo DiCaprio',
            'age': 45,
            'gender': 'male'
	        }

        # sample movie to use in some test cases
        self.new_movie = {
            'title': 'Shutter Island',
            'release_date': '03-10-2010'
	        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    '''
    Test cases
    '''
    def test_retrieve_actors(self):
        #test actors retrieval success
	    res = self.client().get('/actors', headers=auth_header('assistant'))
	    data = json.loads(res.data)

	    self.assertEqual(res.status_code, 200)
	    self.assertEqual(data['success'], True)
	    self.assertTrue(data['actors'])

    def test_401_retrieve_actors(self):
        #test actors retrieval failure - no authorization header
	    res = self.client().post('/actors')
	    data = json.loads(res.data)

	    self.assertEqual(res.status_code, 401)
	    self.assertEqual(data['success'], False)
	    self.assertEqual(data['message'], 'Authorization header is expected.')

    def test_create_actor(self):
        #test actor creation success
	    res = self.client().post('/actors', headers=auth_header('director'), json=self.new_actor)
	    data = json.loads(res.data)

	    self.assertEqual(res.status_code, 200)
	    self.assertEqual(data['success'], True)
	    self.assertTrue(data['actor'])

    def test_403_create_actor(self):
        #test actor creation failure - permission not found
	    res = self.client().post('/actors', headers=auth_header('assistant'), json=self.new_actor)
	    data = json.loads(res.data)

	    self.assertEqual(res.status_code, 403)
	    self.assertEqual(data['success'], False)
	    self.assertEqual(data['message'], 'Permission not found.')

    def test_update_actor(self):
        #test actor update success
	    res = self.client().patch('/actors/7', headers=auth_header('director'), json={'name':'Leonardo Di Caprio'})
	    data = json.loads(res.data)

	    self.assertEqual(res.status_code, 200)
	    self.assertEqual(data['success'], True)
	    self.assertTrue(data['actor'])

    def test_400_update_actor(self):
        #test actor update failure - no body
	    res = self.client().patch('/actors/7', headers=auth_header('director'))
	    data = json.loads(res.data)

	    self.assertEqual(res.status_code, 400)
	    self.assertEqual(data['success'], False)
	    self.assertEqual(data['message'], 'bad request')

    def test_remove_actor(self):
        #test actor removal success
	    res = self.client().delete('/actors/7', headers=auth_header('producer'))
	    data = json.loads(res.data)

	    self.assertEqual(res.status_code, 200)
	    self.assertEqual(data['success'], True)
	    self.assertTrue(data['deleted'])

    def test_422_remove_actor(self):
        #test actor removal failure
	    res = self.client().delete('/actors/1000', headers=auth_header('producer'))
	    data = json.loads(res.data)

	    self.assertEqual(res.status_code, 422)
	    self.assertEqual(data['success'], False)
	    self.assertEqual(data['message'], 'unprocessable')

    def test_retrieve_movies(self):
        #test movies retrieval success
	    res = self.client().get('/movies', headers=auth_header('director'))
	    data = json.loads(res.data)

	    self.assertEqual(res.status_code, 200)
	    self.assertEqual(data['success'], True)
	    self.assertTrue(data['movies'])

    def test_401_retrieve_movies(self):
        #test movies retrieval failure - no authorization header
	    res = self.client().post('/movies')
	    data = json.loads(res.data)

	    self.assertEqual(res.status_code, 401)
	    self.assertEqual(data['success'], False)
	    self.assertEqual(data['message'], 'Authorization header is expected.')

    def test_create_movie(self):
        #test actor creation success
	    res = self.client().post('/movies', headers=auth_header('producer'), json=self.new_movie)
	    data = json.loads(res.data)

	    self.assertEqual(res.status_code, 200)
	    self.assertEqual(data['success'], True)
	    self.assertTrue(data['movie'])

    def test_403_create_movie(self):
        #test movie creation failure - permission not found
	    res = self.client().post('/movies', headers=auth_header('director'), json=self.new_movie)
	    data = json.loads(res.data)

	    self.assertEqual(res.status_code, 403)
	    self.assertEqual(data['success'], False)
	    self.assertEqual(data['message'], 'Permission not found.')

    def test_update_movie(self):
        #test movie update success
	    res = self.client().patch('/movies/7', headers=auth_header('director'), json={'title':'Shutter island'})
	    data = json.loads(res.data)

	    self.assertEqual(res.status_code, 200)
	    self.assertEqual(data['success'], True)
	    self.assertTrue(data['movie'])

    def test_400_update_movie(self):
        #test movie update failure - no body
	    res = self.client().patch('/movies/7', headers=auth_header('director'))
	    data = json.loads(res.data)

	    self.assertEqual(res.status_code, 400)
	    self.assertEqual(data['success'], False)
	    self.assertEqual(data['message'], 'bad request')

    def test_remove_movie(self):
        #test movie removal success
	    res = self.client().delete('/movies/7', headers=auth_header('producer'))
	    data = json.loads(res.data)

	    self.assertEqual(res.status_code, 200)
	    self.assertEqual(data['success'], True)
	    self.assertTrue(data['deleted'])

    def test_422_remove_movie(self):
        #test movie removal failure
	    res = self.client().delete('/movies/1000', headers=auth_header('producer'))
	    data = json.loads(res.data)

	    self.assertEqual(res.status_code, 422)
	    self.assertEqual(data['success'], False)
	    self.assertEqual(data['message'], 'unprocessable')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()