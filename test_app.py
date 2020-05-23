import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie

# set token for different roles
assistant_token='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InJIXzRDcUwxRC01UHVRS0dXOGcwUyJ9.eyJpc3MiOiJodHRwczovL2Nhc3RpbmctYWdlbmN5LWNhcHN0b25lLWZzbmQuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlYzJkZjUwOWMwN2ExMGNlN2M3MmY2NSIsImF1ZCI6IkNhc3RpbmcgQWdlbmN5IiwiaWF0IjoxNTkwMjQ3MjU0LCJleHAiOjE1OTAyNTQ0NTQsImF6cCI6InZ0SmoyNWhtOEkwQ0J1M0FOU3hFT3cxSDVFNzU2emRKIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.SQ1tmNeQR3WPlVU5gyEzmvZV3PdFIsO082LGjQqqxT7C5mN80R2BvDLe4K3-hILh6Tm5JCS2QDFTfs8lZzunFhipDxEcv5JWwbR1QCE2nYDcTLDmIHQ55H3pE-9PjExC3j3NZ3fBFhzrH0HRGIX3Q3Ndg-0kyqD8jNHVhWHAHSdu8JGRHgGZ-7REA8bUI4t6a5s99_7fOKbwLtT3mHX5mNU-Zl6lEaoWqLKiq-Vm9029Qo71lmqPYUEyOLHlxMp04iAFyFpocvEIdQOSXR1GN2wW75lrR-OG8z11MVqNCqFW13fp4frwrBYMzq9cYKpEeCUZdDgKXaDBd3dUV8X0nw'
director_token='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InJIXzRDcUwxRC01UHVRS0dXOGcwUyJ9.eyJpc3MiOiJodHRwczovL2Nhc3RpbmctYWdlbmN5LWNhcHN0b25lLWZzbmQuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlYzJkZmI5NmEzMDU0MGNkOTg0ZTMwZCIsImF1ZCI6IkNhc3RpbmcgQWdlbmN5IiwiaWF0IjoxNTkwMjYwODAwLCJleHAiOjE1OTAyNjgwMDAsImF6cCI6InZ0SmoyNWhtOEkwQ0J1M0FOU3hFT3cxSDVFNzU2emRKIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyJdfQ.dwswLxgyXCCw2otEbFdjZ6p9_FoJIx-88k_Hvjs6lXLAspleUPQg1ImBZ6gd8Kc-wwQtw6oUvCTCLbGtm9HOUTOwZhfr54cRanv4AHiytXWkBs6X9rQPzOAU39eHG4ITmrdhe39p0m03rwP8LTELjR3QUiKQ4Xp7APndETgN5LGEsHOG_zmaSD3di5S6CtnFQNznrYGhCEZEtuP3ZsSBN-k0pqPRC94QJ2ObDwSUzfuWSCGuQq66HKfmswJOD9svejFn8GYJTk6ErgU1--n58uKKIbCCRLrXSLIxcwx7CYv_2zd6iC2x2vznFsHJUchp5JxD2sJ2Lcct7FlmL04lEw'
producer_token='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InJIXzRDcUwxRC01UHVRS0dXOGcwUyJ9.eyJpc3MiOiJodHRwczovL2Nhc3RpbmctYWdlbmN5LWNhcHN0b25lLWZzbmQuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlYzJkZmY2ZDA0N2M5MGNjNTcyNzg5MyIsImF1ZCI6IkNhc3RpbmcgQWdlbmN5IiwiaWF0IjoxNTkwMjYwODkwLCJleHAiOjE1OTAyNjgwOTAsImF6cCI6InZ0SmoyNWhtOEkwQ0J1M0FOU3hFT3cxSDVFNzU2emRKIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.hb-ECTilMLFFRn8tIrT3yyg3OBVoGHfARLv94qG0plNLmBHpJNDBQa4lNheFu86eOb_kkvV1sClefIjwdPp0Ct___iy24cQ4oO_46g80_JPP-7Q38Lw0ysFTMfwy--E7_FsCcYixZ3r9uhObNwY4sI2oaGA4CqlbH74mgWZrWRyhB7jYFVgzkK98j2ew8AQ1ybYN-IV_eUwav740aYKKBhxudQ17Z_wBTrrrhTLCQdgAIL50vWJvsXbKpxpVbU1ThH3qkcaOPtuLUzwEZJJoP82tEGHmAarierKgJlZ6BxgcY0f8hkd_bpTVaHwkqDpq1LLxMl97_9PHjKw77TklEg'
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