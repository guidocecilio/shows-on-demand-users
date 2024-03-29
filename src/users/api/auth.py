# from flask import Blueprint, jsonify, request
# from sqlalchemy import exc, or_

# from users.api.utils import authenticate
# from users.models import User
# from users import db, bcrypt


# auth_blueprint = Blueprint('auth', __name__)


# @auth_blueprint.route('/auth/register', methods=['POST'])
# def register_user():
#     # get post data
#     post_data = request.get_json()
#     if not post_data:
#         response_object = {
#             'status': 'error',
#             'message': 'Invalid payload.'
#         }
#         return jsonify(response_object), 400
#     username = post_data.get('username')
#     email = post_data.get('email')
#     password = post_data.get('password')
#     try:
#         # check for existing user
#         user = User.query.filter(
#             or_(User.username == username, User.email==email)).first()
#         if not user:
#             # add new user to db
#             new_user = User(
#                 username=username,
#                 email=email,
#                 password=password
#             )
#             db.session.add(new_user)
#             db.session.commit()
#             # generate auth token
#             auth_token = new_user.encode_auth_token(new_user.id)
#             response_object = {
#                 'status': 'success',
#                 'message': 'Successfully registered.',
#                 'auth_token': auth_token.decode()
#             }
#             return jsonify(response_object), 201
#         else:
#             response_object = {
#                 'status': 'error',
#                 'message': 'Sorry. That user already exists.'
#             }
#             return jsonify(response_object), 400
#     # handler errors
#     except (exc.IntegrityError, ValueError) as e:
#         db.session().rollback()
#         response_object = {
#             'status': 'error',
#             'message': 'Invalid payload.'
#         }
#         return jsonify(response_object), 400


# @auth_blueprint.route('/auth/login', methods=['POST'])
# def login_user():
#     # get post data
#     post_data = request.get_json()
#     if not post_data:
#         response_object = {
#             'status': 'error',
#             'message': 'Invalid payload.'
#         }
#         return jsonify(response_object), 400
#     email = post_data.get('email')
#     password = post_data.get('password')
#     try:
#         # fetch the user data
#         user = User.query.filter_by(email=email).first()
#         if user and bcrypt.check_password_hash(user.password, password):
#             auth_token = user.encode_auth_token(user.id)
#             if auth_token:
#                 response_object = {
#                     'status': 'success',
#                     'message': 'Successfully logged in.',
#                     'auth_token': auth_token.decode()
#                 }
#                 return jsonify(response_object), 200
#         else:
#             response_object = {
#                 'status': 'error',
#                 'message': 'User does not exist.'
#             }
#             return jsonify(response_object), 404
#     except Exception as e:
#         print(e)
#         response_object = {
#             'status': 'error',
#             'message': 'Try again.'
#         }
#         return jsonify(response_object), 500


# @auth_blueprint.route('/auth/logout', methods=['GET'])
# @authenticate
# def logout_user(resp):
#     response_object = {
#         'status': 'success',
#         'message': 'Successfully logged out.'
#     }
#     return jsonify(response_object), 200


# @auth_blueprint.route('/auth/status', methods=['GET'])
# @authenticate
# def get_user_status(resp):
#     user = User.query.filter_by(id=resp).first()
#     response_object = {
#         'status': 'success',
#         'data': {
#             'id': user.id,
#             'username': user.username,
#             'email': user.email,
#             'active': user.active,
#             'created_at': user.created_at
#         }
#     }
#     return jsonify(response_object), 200

from flask_restplus import Namespace, fields
from flask import request
from flask_restplus import Resource

from users import db
from users.models import User, BlacklistToken
from users.services import Auth

ns = Namespace('auth', description='Authentication related operations')
user_auth = ns.model('auth_details', {
    'email': fields.String(required=True, description='The email address'),
    'password': fields.String(required=True, description='The user password '),
})


@ns.route('/login')
class UserLogin(Resource):
    """
    User Login Resource
    """
    @ns.doc('user login')
    @ns.expect(user_auth, validate=True)
    def post(self):
        # get the post data
        post_data = request.json
        return Auth.login_user(data=post_data)


@ns.route('/logout')
class LogoutAPI(Resource):
    """
    Logout Resource
    """
    @ns.doc('logout a user')
    def post(self):
        # get auth token
        auth_header = request.headers.get('Authorization')
        return Auth.logout_user(data=auth_header)