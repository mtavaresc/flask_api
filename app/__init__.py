from flask import request, jsonify, abort
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy

from instance.config import app_config

db = SQLAlchemy()


def create_app(config_name):
    from app.models import User
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    @app.route('/users/', methods=['GET', 'POST'])
    def users():
        if request.method == 'POST':
            username = str(request.data.get('username', ''))
            password = str(request.data.get('password', ''))

            if User.get_by_username(username):
                response = jsonify({'message': f'User {username} already exists'})
                response.status_code = 200
                return response

            try:
                new_user = User(username=username, password=User.generate_hash(password))
                new_user.save()
                response = jsonify({
                    'id': new_user.id,
                    'username': new_user.username,
                    'password': new_user.password,
                    'date_created': new_user.date_created,
                    'date_modified': new_user.date_modified
                })
                response.status_code = 201
            except Exception as e:
                response = jsonify({'message': f'Something went wrong: {e}'})
                response.status_code = 500

            return response
        else:
            # GET
            buckets = User.get_all()
            results = []

            for user in buckets:
                obj = {
                    'id': user.id,
                    'username': user.username,
                    'password': user.password,
                    'date_created': user.date_created,
                    'date_modified': user.date_modified
                }
                results.append(obj)
            response = jsonify(results)
            response.status_code = 200
            return response

    @app.route('/users/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
    def users_manipulation(user_id):
        # retrieve a user using it's ID
        user = User.query.filter_by(id=user_id).first()
        if not user:
            # Raise an HTTPException with a 404 not found status code
            abort(404)
        if request.method == 'DELETE':
            user.delete()
            return {'message': f'User {user.username} deleted successfully'}, 200
        elif request.method == 'PUT':
            username = str(request.data.get('username', ''))
            password = str(request.data.get('password', ''))
            user.username = username
            user.password = password
            user.save()
            response = jsonify({
                'id': user.id,
                'username': user.username,
                'password': user.password,
                'date_created': user.date_created,
                'date_modified': user.date_modified
            })
            response.status_code = 200
            return response
        else:
            # GET
            response = jsonify({
                'id': user.id,
                'username': user.username,
                'password': user.password,
                'date_created': user.date_created,
                'date_modified': user.date_modified
            })
            response.status_code = 200
            return response

    return app
