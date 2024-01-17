import os

SECRET_KEY = 'alura'

SQLALCHEMY_DATABASE_URI = \
    '{SGBD}://{user}:{password}@{host}/{db}'.format(
        SGBD = 'mysql+mysqlconnector',
        user = 'gameteca',
        password = '12345678',
        host = '127.0.0.1',
        db = 'gameteca'
    )

UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__)) + '/uploads'