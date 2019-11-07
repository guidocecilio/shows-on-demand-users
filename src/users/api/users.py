import uuid
import datetime

from flask import request
from flask_restplus import Resource
from flask_restplus import Namespace, fields

from users import db
from users.models import User
from users.util.decorator import admin_token_required

# from users import constants, models, settings, exceptions, utils
# KEY_USER_ID = 'id'
# KEY_USER_USERNAME = 'username'
# KEY_USER_EMAIL = 'email'
# KEY_USER_PASSWORD = 'password'
# KEY_USER_ACTIVE = 'active'
# KEY_USER_ADMIN = 'admin'
# KEY_USER_CREATED_AT = 'created_at'

ns = Namespace('user', description='User CRUD operations, encapsulates the operations for users manipulation')
user_schema = ns.model('user', {
    'email': fields.String(required=True, description='user email address'),
    'username': fields.String(required=True, description='user username'),
    'password': fields.String(required=True, description='user password'),
    'public_id': fields.String(description='user Identifier')
})

def save_new_user(data):
    user = User.query.filter_by(email=data['email']).first()
    if not user:
        new_user = User(
            public_id=str(uuid.uuid4()),
            email=data['email'],
            username=data['username'],
            password=data['password'],
            registered_on=datetime.datetime.utcnow()
        )
        save_changes(new_user)
        return generate_token(new_user)
    else:
        response_object = {
            'status': 'fail',
            'message': 'User already exists. Please Log in.',
        }
        return response_object, 409


def get_all_users():
    return User.query.all()


def get_a_user(public_id):
    return User.query.filter_by(public_id=public_id).first()


def generate_token(user):
    try:
        # generate the auth token
        auth_token = User.encode_auth_token(user.id)
        response_object = {
            'status': 'success',
            'message': 'Successfully registered.',
            'Authorization': auth_token.decode()
        }
        return response_object, 201
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.'
        }
        return response_object, 401


def save_changes(data):
    db.session.add(data)
    db.session.commit()

@ns.route('', methods=['GET', 'POST', ], endpoint='user-list')
class UserList(Resource):
    @ns.doc('list_of_registered_users')
    @admin_token_required
    @ns.marshal_list_with(user_schema, envelope='data')
    def get(self):
        """List all registered users"""
        return get_all_users()

    @ns.expect(user_schema, validate=True)
    @ns.response(201, 'User successfully created.')
    @ns.doc('create a new user')
    def post(self):
        """Creates a new User """
        data = request.json
        return save_new_user(data=data)


@ns.route('/<public_id>', methods=['GET', 'PATCH', 'DELETE', ], endpoint='user-details')
@ns.param('public_id', 'The User identifier')
@ns.response(404, 'User not found.')
class User(Resource):
    @ns.doc('get a user')
    @ns.marshal_with(user_schema)
    def get(self, public_id):
        """get a user given its identifier"""
        user = get_a_user(public_id)
        if not user:
            ns.abort(404)
        else:
            return user
