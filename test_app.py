import os
import unittest
import json
from app import create_app
from models import setup_db, Movies, Actors
from flask_sqlalchemy import SQLAlchemy

ExecutiveProducer = os.environ.get('EXECUTIVE_PRODUCER')
CastingDirector = os.environ.get('CASTING_DIRECTOR')
CastingAssistant = os.environ.get('CASTING_ASSISTANT')

#The Cating Agency test case class
class CatingAgencyTestCase(unittest.TestCase):
    def setUp(self):
        #Define test variables and initialize app
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = os.environ.get('TEST_DATABASE_URL')
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # self.db.create_all()

            self.new_movie = {
                "title": "Spider-man",
                "release_date": "2002-04-29"
            }

            self.new_actor = {
                "name": "xxx",
                "age": 30,
                "gender": "female"
            }

            self.update_movie = {
                "title": "Inception",
                "release_date": "2010-07-08"
            }

            self.update_actor = {
                "name": "leonardo dicaprio",
                "age": 46,
                "gender": "male"
            }

    def tearDown(self):
        """Executed after reach test"""
        pass



    ##TESTS OF SUCCESS FOR ALL ENDPOINTS:
    #####################################

    # test for the success of retrieving the movies
    def test_get_movies(self):
        res = self.client().get('/movies', headers={'Authorization': 'Bearer {}'.format(CastingAssistant)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["movies"])

    # test for the success of retrieving the actors
    def test_get_actors(self):
        res = self.client().get('/actors', headers={'Authorization': 'Bearer {}'.format(CastingAssistant)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["actors"])

    # test for the success of adding movies
    def test_create_movies(self):
        res = self.client().post('/movies', json=self.new_movie, headers={'Authorization': 'Bearer {}'.format(ExecutiveProducer)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['new_movies'])

    # test for the success of adding actors
    def test_create_actors(self):
        res = self.client().post('/actors', json=self.new_actor, headers={'Authorization': 'Bearer {}'.format(ExecutiveProducer)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['new_actors'])

    # test for the success of updating movies
    def test_update_movies(self):
        res = self.client().patch('/movies/2', json=self.update_movie, headers= {'Authorization': 'Bearer {}'.format(CastingDirector)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['updated_movie'])

    # test for the success of updating actors
    def test_update_actors(self):
        res = self.client().patch('/actors/2', json=self.update_actor, headers= {'Authorization': 'Bearer {}'.format(CastingDirector)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['updated_actor'])

    # test for the success of deleting movies
    def test_delete_movies(self):
        res = self.client().delete('/movies/3', headers= {'Authorization': 'Bearer {}'.format(ExecutiveProducer)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted_movie'])

    # test for the success of deleting actors
    def test_delete_actors(self):
        res = self.client().delete('/actors/3', headers= {'Authorization': 'Bearer {}'.format(ExecutiveProducer)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted_actor'])





    ##TESTS OF ERROR BEHAVIOR FOR ALL ENDPOINTS
    ###########################################

    # test for (AuthError) when try to get movies
    def test_401_get_movies(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    # test for (AuthError) when try to get actors
    def test_401_get_actors(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    # test for (resource not found) when try to post movies
    def test_404_create_movies(self):
        res = self.client().post('/movies', json={}, headers= {'Authorization': 'Bearer {}'.format(ExecutiveProducer)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], 'resource not found')

    # test for (resource not found) when try to post actors
    def test_404_create_actors(self):
        res = self.client().post('/actors', json={}, headers= {'Authorization': 'Bearer {}'.format(CastingDirector)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], 'resource not found')

    # test for (bad request) when try to update movies
    def test_400_update_movies(self):
        res = self.client().patch('/movies/2', json=None, headers= {'Authorization': 'Bearer {}'.format(CastingDirector)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], 'bad request')

    # test for (bad request) when try to update actors
    def test_400_update_actors(self):
        res = self.client().patch('/actors/2', json=None, headers= {'Authorization': 'Bearer {}'.format(ExecutiveProducer)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], 'bad request')

    # test for (AuthError) when try to delete movies
    def test_401_delete_movies(self):
        res = self.client().delete('movies/2', headers= {'Authorization': 'Bearer {}'.format(CastingAssistant)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)


    # test for (resource not found) when try to delete actors
    def test_404_delete_actors(self):
        res = self.client().delete('/actors/10000', headers= {'Authorization': 'Bearer {}'.format(ExecutiveProducer)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], 'resource not found')



if __name__ == "__main__":
    unittest.main()
