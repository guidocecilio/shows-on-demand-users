import os

from flask import Flask, jsonify, Blueprint
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
import flask_restplus
from werkzeug.contrib import fixers


# instantiate the extensions
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()

def register_api(_app):
    from users.api.users import ns as users_ns
    from users.api.auth import ns as auth_ns

    blueprint = Blueprint('api', __name__)
    api = flask_restplus.Api(
        app=blueprint,
        doc=_app.config['SWAGGER_PATH'],
        version=_app.config['API_VERSION'],
        title='Shows On Demand - Users Service REST API',
        description='Shows on deman Users service API for users access.',
        validate=_app.config['RESTPLUS_VALIDATE']
    )
    api.add_namespace(auth_ns, path='/{}/auth'.format(_app.config['API_VERSION']))
    api.add_namespace(users_ns, path='/{}/users'.format(_app.config['API_VERSION']))
    _app.register_blueprint(blueprint)


def create_app():
    # instantiate the app
    app = Flask(__name__)

    # enable CORS
    CORS(app)

    # set config
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)
    app_config = app.config

    # set up extensions
    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)

    app.wsgi_app = fixers.ProxyFix(app.wsgi_app)

    # register blueprints
    register_api(app)
    return app
