import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from models import setup_db, Actor, Movie
from auth import AuthError, requires_auth


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    '''
    Routes
    '''

    '''
    Actors
    '''
    @app.route('/actors')
    @requires_auth('get:actors')
    def get_actors(payload):
        actors = Actor.query.all()

        if len(actors) == 0:
            abort(404)

        return jsonify({
                'success': True,
                'actors': [actor.format() for actor in actors]
            }), 200

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def create_actor(payload):
        body = request.get_json()

        if body is None:
            abort(400)

        try:
            new_name = body.get('name', None)
            new_age = body.get('age', None)
            new_gender = body.get('gender', None)

            actor = Actor(name=new_name, age=new_age, gender=new_gender)

            actor.insert()

            return jsonify({
                    'success': True,
                    'actor': actor.format()
                }), 200

        except:
            abort(422)

    @app.route('/actors/<int:id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actor(payload, id):
        body = request.get_json()

        try:
            actor = Actor.query.filter(Actor.id == id).one_or_none()
            if actor is None:
                abort(404)

            updated_name = body.get('name', None)
            updated_age = body.get('age', None)
            updated_gender = body.get('gender', None)

            if updated_name:  # check if name was updated
                actor.name = updated_name

            if updated_age:  # check if age was updated
                actor.age = updated_age

            if updated_gender:  # check if gender was updated
                actor.gender = updated_gender

            actor.update()

            return jsonify({
                    'success': True,
                    'actor': actor.format()
                }), 200

        except:
            abort(400)

    @app.route('/actors/<int:id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def remove_actor(payload, id):
        try:
            actor = Actor.query.filter(Actor.id == id).one_or_none()
            if actor is None:
                abort(404)

            actor.delete()

            return jsonify({
                    'success': True,
                    'deleted': actor.id
                })

        except:
            abort(422)

    '''
    Movies
    '''
    @app.route('/movies')
    @requires_auth('get:movies')
    def get_movies(payload):
        movies = Movie.query.all()

        if len(movies) == 0:
            abort(404)

        return jsonify({
                'success': True,
                'movies': [movie.format() for movie in movies]
            }), 200

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def create_movie(payload):
        body = request.get_json()

        if body is None:
            abort(400)

        try:
            new_title = body.get('title', None)
            new_release_date = body.get('release_date', None)

            movie = Movie(title=new_title, release_date=new_release_date)

            movie.insert()

            return jsonify({
                    'success': True,
                    'movie': movie.format()
                }), 200

        except:
            abort(422)

    @app.route('/movies/<int:id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movie(payload, id):
        body = request.get_json()

        try:
            movie = Movie.query.filter(Movie.id == id).one_or_none()
            if movie is None:
                abort(404)

            updated_title = body.get('title', None)
            updated_release_date = body.get('release_date', None)

            if updated_title:  # check if title was updated
                movie.title = updated_title

            if updated_release_date:  # check if release date was updated
                movie.release_date = updated_release_date

            movie.update()

            return jsonify({
                    'success': True,
                    'movie': movie.format()
                }), 200

        except:
            abort(400)

    @app.route('/movies/<int:id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def remove_movie(payload, id):
        try:
            movie = Movie.query.filter(Movie.id == id).one_or_none()
            if movie is None:
                abort(404)

            movie.delete()

            return jsonify({
                    'success': True,
                    'deleted': movie.id
                })

        except:
            abort(422)

    '''
    Error Handlers
    '''
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
                'success': False,
                'error': 400,
                'message': 'bad request'
            }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
                'success': False,
                'error': 404,
                'message': 'resource not found'
            }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
                "success": False,
                "error": 422,
                "message": "unprocessable"
            }), 422

    @app.errorhandler(AuthError)
    def auth_error(AuthError):
        return jsonify({
                "success": False,
                "error": AuthError.status_code,
                "message": AuthError.error['description']
            }), AuthError.status_code

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
