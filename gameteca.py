# region Imports

from flask import Flask

from flask_sqlalchemy import SQLAlchemy

from flask_wtf.csrf import CSRFProtect

from flask_bcrypt import Bcrypt

# endregion


app = Flask(__name__)

app.config.from_pyfile('config.py')

db = SQLAlchemy(app)
csrf = CSRFProtect(app)
bcrypt = Bcrypt(app)

from routes.auth import *
from routes.crud import *

if __name__ == "__main__":
    app.run(debug=True)
