import os
import unittest
import json
from app import create_app
from models import setup_db, Movies, Actors
from flask_sqlalchemy import SQLAlchemy

ExecutiveProducer = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IldOQVNSTm9sVkxOWmFkd1pHQWdmVSJ9.eyJpc3MiOiJodHRwczovL3NhbGVoLWRldi51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjEyMmU0ZGFhZWJiNGEwMDY5OThhNDZmIiwiYXVkIjoiYWdlbmN5IiwiaWF0IjoxNjMwMjExOTI1LCJleHAiOjE2MzAyMTkxMjUsImF6cCI6IlJ0U1pYMDNmTkQ0U3d5SmFnTHJobUNsTzdxM2JqSWVaIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.lTYahDRmfIDNjfzrW2iVXUwxYKdPQpOYl-VIgrOZk4brJ1_CtyJ1BHZQpSZGaaBdQbRddm8t5Vr8muRaIJAjL_JyGnuvPNpcA46OyDSZEQk-qz4BGbLmsZBmCuZTz9fQvvz7rAurgilD6j8puL5w8sqepVa1hrVYrwOFZ7PWbXDal4JdF3cLQi_Z_UB8QwrYvbBvLbyMbG5ejZGR66a2BwmsgSfT16v7bD09y1rax5shG3Ofdvhv-Ux4b_smPjcQy07EMopVMbZGUGR48nNgLVgVe4zspUKwnwCDuj4hAudikgKol6guVXN_SJqREpLyZMpq8zx0omGNC2m7-lYDRg'
CastingDirector = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IldOQVNSTm9sVkxOWmFkd1pHQWdmVSJ9.eyJpc3MiOiJodHRwczovL3NhbGVoLWRldi51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjEyMmVlNWVkNzIwYmMwMDY5YjlhNDE1IiwiYXVkIjoiYWdlbmN5IiwiaWF0IjoxNjMwMjExOTcxLCJleHAiOjE2MzAyMTkxNzEsImF6cCI6IlJ0U1pYMDNmTkQ0U3d5SmFnTHJobUNsTzdxM2JqSWVaIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyJdfQ.Ns_u1Uj8bS9ln-DUGj2LzO1ueQEeoG4IuK-M04qEjl5bgNi9_z0rsD9gHE_4y5_00ENNVw2YbDelXx-nQvwOK7r9LR5eSmjyR6zvNlG622iazTNt0WXgqhkodPz0vInTeI3PnRctr0WNPBoVL6LaYuI6P-63xSohBuMzlhtZTNg0ZITTXjVF7fayO8DPyA7f6OwOO1E5S2iU_Fb4Kqit_l_JVRNzIOnJjD904vRBpBS4k4D58R9C4HAlTZ--BvxLN6V-OOWppzBfYSrDhW4kxFA2QRlFQ2iDBdPp8QbRVlPaUap2_eKbzOTjfI1IGwueZtxRR5tEepEHY8KNoR0mKw'
CastingAssistant = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IldOQVNSTm9sVkxOWmFkd1pHQWdmVSJ9.eyJpc3MiOiJodHRwczovL3NhbGVoLWRldi51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjEyMmVlMjliNTQwZGQwMDZiMmQwZjAxIiwiYXVkIjoiYWdlbmN5IiwiaWF0IjoxNjMwMjEyMDE3LCJleHAiOjE2MzAyMTkyMTcsImF6cCI6IlJ0U1pYMDNmTkQ0U3d5SmFnTHJobUNsTzdxM2JqSWVaIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.QHLoUcj-gWzT2ZIY4QfnyJjlbVPsMkoX1gatH1YHsu1qdj8qGzyMEOJRLqihPQBHK7fX6tdl3kJZy27ZDw0iybQ-kIHwcQM40dZD6LuCQWlVMkUhDmD5N7tlHGvi2GGXGIjZgShyXTMLps6Ez29oZoyrDPjAuYTaFHDhEyQVBXPw0LSCNDSu5JAsyO4RSoj0HcLfclmO35816FaBfcHIgS-RATcZu7YOar5zlmTncX37TILZqzrzMq0Mbkp9fDag78TJHLvjWOfRRX8iTWwh8Vc6lyhj-C4xsslQxpoZ4ELox9ONvdCe_WhCAasx_3yYNb9NZHnL41mQ_Os1VXiQsw'


class CatingAgencyTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = os.environ.get('TEST_DATABASE_URL')
        setup_db(self.app, self.database_path)

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



    # TESTS OF SUCCESS FOR ALL ENDPOINTS:
    ###################################
    def test_get_movies(self):
        res = self.client().get('/movies', headers={'Authorization': 'Bearer {}'.format(CastingAssistant)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["movies"])

    def test_get_actors(self):
        res = self.client().get('/actors', headers={'Authorization': 'Bearer {}'.format(CastingAssistant)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["actors"])

    def test_create_movies(self):
        res = self.client().post('/movies', json=self.new_movie, headers={'Authorization': 'Bearer {}'.format(ExecutiveProducer)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['new_movies'])

    def test_create_actors(self):
        res = self.client().post('/actors', json=self.new_actor, headers={'Authorization': 'Bearer {}'.format(ExecutiveProducer)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['new_actors'])


    def test_update_movies(self):
        res = self.client().patch('/movies/2', json=self.update_movie, headers= {'Authorization': 'Bearer {}'.format(CastingDirector)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['updated_movie'])


    def test_update_actors(self):
        res = self.client().patch('/actors/2', json=self.update_actor, headers= {'Authorization': 'Bearer {}'.format(CastingDirector)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['updated_actor'])


    def test_delete_movies(self):
        res = self.client().delete('/movies/3', headers= {'Authorization': 'Bearer {}'.format(ExecutiveProducer)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted_movie'])


    def test_delete_actors(self):
        res = self.client().delete('/actors/3', headers= {'Authorization': 'Bearer {}'.format(ExecutiveProducer)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted_actor'])





    # TESTS OF ERROR BEHAVIOR FOR ALL ENDPOINTS
    ###########################################

    def test_401_get_movies(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_401_get_actors(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)


    def test_404_create_movies(self):
        res = self.client().post('/movies', json={}, headers= {'Authorization': 'Bearer {}'.format(ExecutiveProducer)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], 'resource not found')

    def test_404_create_actors(self):
        res = self.client().post('/actors', json={}, headers= {'Authorization': 'Bearer {}'.format(CastingDirector)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], 'resource not found')


    def test_400_update_movies(self):
        res = self.client().patch('/movies/2', json=None, headers= {'Authorization': 'Bearer {}'.format(CastingDirector)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], 'bad request')


    def test_400_update_actors(self):
        res = self.client().patch('/actors/2', json=None, headers= {'Authorization': 'Bearer {}'.format(ExecutiveProducer)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], 'bad request')


    def test_401_delete_movies(self):
        res = self.client().delete('movies/2', headers= {'Authorization': 'Bearer {}'.format(CastingAssistant)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)



    def test_404_delete_actors(self):
        res = self.client().delete('/actors/10000', headers= {'Authorization': 'Bearer {}'.format(ExecutiveProducer)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], 'resource not found')



if __name__ == "__main__":
    unittest.main()
