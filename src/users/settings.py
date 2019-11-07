from os import environ

LOG_LEVEL = environ.get('LOG_LEVEL') or 'INFO'

HOST = environ.get('HOST', '0.0.0.0')
SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URL')

# Flask-Restplus settings
RESTPLUS_VALIDATE = environ.get('API_VALIDATE', True)
SWAGGER_PATH = environ.get('SWAGGER_PATH', '/api-docs/')

def get_var(var_name, default=None):
    if var_name in environ:
        return environ[var_name]

    return globals().get(var_name, default)