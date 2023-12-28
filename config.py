import os

SECRET_KEY = 'alura'

SQLALCHEMY_DATABASE_URI = \
    '{SGBD}://{user}:{password}@{host}/{db}'.format(
        SGBD = 'mysql+mysqlconnector',
        user = 'wsl_root',
        password = 'capreo9709',
        host = '127.0.0.1',
        db = 'gameteca'
    )

UPLOAD_PATH = os.path.dirname(os.path.realpath(__file__)) + '/content'