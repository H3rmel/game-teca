SECRET_KEY = 'alura'

SQLALCHEMY_DATABASE_URI = \
    '{SGBD}://{user}:{password}@{host}/{db}'.format(
        SGBD = 'mysql+mysqlconnector',
        user = 'wsl_root',
        password = 'capreo9709',
        host = '127.0.0.1',
        db = 'gameteca'
    )