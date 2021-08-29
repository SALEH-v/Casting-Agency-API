import os

import requests
from flask import Flask, request, abort, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import *
from auth import AuthError, requires_auth
import json


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Allow-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Allow-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')

        return response

    @app.route('/')
    def indexPage():
        return render_template("index.html")

    @app.route('/login-result')
    def LoginResult():
        return render_template('login_result.html')

    @app.route('/logout')
    def Logout():
        return render_template('logout.html')



    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies(payload):
        movies = Movies.query.all()
        if len(movies) == 0:
            abort(400)
        formatedMovies = [movie.format() for movie in movies]

        return jsonify({
            'success': True,
            'movies': formatedMovies
        }), 200

    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors(payload):
        actors = Actors.query.all()
        if len(actors) == 0:
            abort(400)
        formatedActors = [actor.format() for actor in actors]

        return jsonify({
            'success': True,
            'actors': formatedActors
        }), 200

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def post_movie(payload):
        movies_body = request.get_json()
        if movies_body is None:
            abort(400)

        try:
            title = movies_body.get('title')
            release_date = movies_body.get('release_date')

            if (title is None) or (release_date is None):
                abort(400)

            movies = Movies(title=title, release_date=release_date)

            movies.insert()


        except Exception as e:
            print(e)
            abort(404)

        return jsonify({
            'success': True,
            'new_movies': [movies.format()]
        })

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def add_actors(payload):
        actors_body = request.get_json()
        if actors_body is None:
            abort(400)

        try:
            name = actors_body.get('name')
            age = actors_body.get('age')
            gender = actors_body.get('gender')

            if (name is None) or (age is None) or (gender is None):
                abort(400)

            actors = Actors(name=name, age=age, gender=gender)
            actors.insert()

        except Exception as e:
            print(e)
            abort(404)

        return jsonify({
            'success': True,
            'new_actors': [actors.format()]
        }), 200

    @app.route('/movies/<id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movies(payload, id):
        movies_body = request.get_json()
        if movies_body is None:
            abort(400)

        movie = Movies.query.get(id)
        if not movie:
            abort(404)
        try:
            title = movies_body.get('title')
            release_date = movies_body.get('release_date')

            movie.title = title
            movie.release_date = release_date

            movie.update()
        except Exception as e:
            print(e)
            abort(500)

        return jsonify({
            'success': True,
            'updated_movie': [movie.format()]
        }), 200

    @app.route('/actors/<id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actors(payload, id):
        actors_body = request.get_json()
        if actors_body is None:
            abort(400)

        actor = Actors.query.get(id)
        if not actor:
            abort(404)
        try:
            name = actors_body.get('name')
            age = actors_body.get('age')
            gender = actors_body.get('gender')

            actor.name = name
            actor.age = age
            actor.gender = gender

            actor.update()
        except Exception as e:
            print(e)
            abort(500)

        return jsonify({
            'success': True,
            'updated_actor': [actor.format()]
        }), 200

    @app.route('/movies/<id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movies(payload, id):
        movie = Movies.query.get(id)

        if not movie:
            abort(404)

        try:
            movie.delete()
        except Exception as e:
            print(e)
            abort(500)

        return jsonify({
            "success": True,
            "deleted_movie": [movie.format()]
        }), 200

    @app.route('/actors/<id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actors(payload, id):
        actor = Actors.query.get(id)

        if not actor:
            abort(404)

        try:
            actor.delete()
        except Exception as e:
            print(e)
            abort(500)

        return jsonify({
            "success": True,
            "deleted_actor": [actor.format()]
        }), 200

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': "resource not found"
        }), 404

    @app.errorhandler(AuthError)
    def authError(error):
        errorCode = error.status_code
        messageDescription = error.error['description']

        return jsonify({
            'success': False,
            'error': errorCode,
            'message': messageDescription
        }), 401


    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal server error"
        }), 500


    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Method not allowed"
        }), 405

    return app


app = create_app()

if __name__ == '__main__':
    app.run()
