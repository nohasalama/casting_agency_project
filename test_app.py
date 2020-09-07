import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie

# set token for different roles
assistant_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InJIXzRDcUwxRC01UHVRS0dXOGcwUyJ9.eyJpc3MiOiJodHRwczovL2Nhc3RpbmctYWdlbmN5LWNhcHN0b25lLWZzbmQuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlYzJkZjUwOWMwN2ExMGNlN2M3MmY2NSIsImF1ZCI6IkNhc3RpbmcgQWdlbmN5IiwiaWF0IjoxNTkwMzA3ODc3LCJleHAiOjE1OTAzMTUwNzcsImF6cCI6InZ0SmoyNWhtOEkwQ0J1M0FOU3hFT3cxSDVFNzU2emRKIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.qwkvaKJvQ66jqM0Dil-YXPWEeLn_0qVhm0vdvhM7ClKiq_Q74s2X5RHge0TrcFSgwLvuQDh6WGLg8wsDdTpElaCnuYUIsssVg5RS8sJ8cIyBTPRyhf67J78t50j5zk-x6ov2OzxY_ReSZSgDCMqOxgY-_AR0mn0wyuJZoj6f5x_3B86s-1OlylPTOs8mEaNj6HXQfWDaJKmxTcIfG74rAfljxtcq6swmfQ638Y6J8Rd2wUbKryMjFQ_Cd-WUC-fdP8uFurFxax9PSdrNandyWck1y5zgN0Uf86uf8Zdh1NqzOUiIdsfYu9sPvseM0SOC4Bz7JPcRr1fGwB_KGIQ3rA'
director_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InJIXzRDcUwxRC01UHVRS0dXOGcwUyJ9.eyJpc3MiOiJodHRwczovL2Nhc3RpbmctYWdlbmN5LWNhcHN0b25lLWZzbmQuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlYzJkZmI5NmEzMDU0MGNkOTg0ZTMwZCIsImF1ZCI6IkNhc3RpbmcgQWdlbmN5IiwiaWF0IjoxNTkwMzA4MDgzLCJleHAiOjE1OTAzMTUyODMsImF6cCI6InZ0SmoyNWhtOEkwQ0J1M0FOU3hFT3cxSDVFNzU2emRKIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyJdfQ.YAZryLxqfCv22RzTjWf-BCEmfKCpBN5lmhz6YBf44Hj-dIZwJ-9U6Q_PIfutNXti1KFTRuk2KQrILOTcOq4J3CP1DYZShiCksJXRajrSA0frWLUo21tpbh7DfLx9hgcYASn2cDUKfK4HYI_QQThfdyxyfWFpeecYIdFNXPg8NsWiZXE0vN_dUn5S6tpXmua_atXbE2gfzHwlT9aTI1UaPEMYRMN1ULfCJj62gaomIy21pnZaWrAtK0yKdvDT-C4sWZZukSvD2J8l-WQhjCMn4a-VlUZaihbO584zSllfDyf9SCaSMoBb_cru-MIbzpvet-HVtOq7XTRv7a1Ealdfvw'
producer_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InJIXzRDcUwxRC01UHVRS0dXOGcwUyJ9.eyJpc3MiOiJodHRwczovL2Nhc3RpbmctYWdlbmN5LWNhcHN0b25lLWZzbmQuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlYzJkZmY2ZDA0N2M5MGNjNTcyNzg5MyIsImF1ZCI6IkNhc3RpbmcgQWdlbmN5IiwiaWF0IjoxNTkwMzA4MTcxLCJleHAiOjE1OTAzMTUzNzEsImF6cCI6InZ0SmoyNWhtOEkwQ0J1M0FOU3hFT3cxSDVFNzU2emRKIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.lVqPyK4yHNlSCSYGH_4V2FGPPrIWuYKyE1AJaJiVEDevMQuCO2YwzhKxl27bYDPGFrATA0KU7U_NZCUv7K7m9C4avw9gRbs21vE2GunlXI-zSddFQ18gIJIFw1LnR9OLPzSu1ryNsBX3820sXUO3no3M2XO8z0vH_iDxIfM_KsozfyifrG6vdNiUaOxvTrQKIj6J4AHtk2BBEvhMiJ7zhPuCyVfbJdIbLWtxhKvULcQ8Z9po91TNAqCbXtPgvDwQT2xiuH4Nd-7bhmOw74qJDXutG9OhbmDeuZlVXl-CVLOlJf3R7FQwOO4uratgeK6J1Zh9gqDqAQAx2_mV2QlWjw'


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
        self.database_path = "postgres://{}:{}@{}/{}".format('postgres', 'postgres', 'localhost:5432', self.database_name)
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
        # test actors retrieval success
        res = self.client().get('/actors', headers=auth_header('assistant'))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    def test_401_retrieve_actors(self):
        # test actors retrieval failure - no authorization header
        res = self.client().post('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Authorization header is expected.')

    def test_create_actor(self):
        # test actor creation success
        res = self.client().post('/actors', headers=auth_header('director'), json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])

    def test_403_create_actor(self):
        # test actor creation failure - permission not found
        res = self.client().post('/actors', headers=auth_header('assistant'), json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')

    def test_update_actor(self):
        # test actor update success
        res = self.client().patch('/actors/7', headers=auth_header('director'), json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])

    def test_400_update_actor(self):
        # test actor update failure - no body
        res = self.client().patch('/actors/6', headers=auth_header('director'))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    def test_remove_actor(self):
        # test actor removal success
        res = self.client().delete('/actors/6', headers=auth_header('producer'))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted'])

    def test_422_remove_actor(self):
        # test actor removal failure
        res = self.client().delete('/actors/1000', headers=auth_header('producer'))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_retrieve_movies(self):
        # test movies retrieval success
        res = self.client().get('/movies', headers=auth_header('director'))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test_401_retrieve_movies(self):
        # test movies retrieval failure - no authorization header
        res = self.client().post('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Authorization header is expected.')

    def test_create_movie(self):
        # test actor creation success
        res = self.client().post('/movies', headers=auth_header('producer'), json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])

    def test_403_create_movie(self):
        # test movie creation failure - permission not found
        res = self.client().post('/movies', headers=auth_header('director'), json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')

    def test_update_movie(self):
        # test movie update success
        res = self.client().patch('/movies/6', headers=auth_header('director'), json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])

    def test_400_update_movie(self):
        # test movie update failure - no body
        res = self.client().patch('/movies/6', headers=auth_header('director'))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    def test_remove_movie(self):
        # test movie removal success
        res = self.client().delete('/movies/7', headers=auth_header('producer'))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted'])

    def test_422_remove_movie(self):
        # test movie removal failure
        res = self.client().delete('/movies/1000', headers=auth_header('producer'))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
