from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_admin import Admin

app = Flask(__name__)

CORS(app)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://tztkrkcgvulyve:3e9432baa140f37bd2702a7655e72dc0b9a1fd302d56147b71bed445ac252274@ec2-34-199-68-114.compute-1.amazonaws.com:5432/d9bt31216sb5kl'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "sadjfkadfa09234"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
admin = Admin(app)
login_manager = LoginManager(app)
login_manager.login_view = "access_denied"
login_manager.login_message = "Access Denied!"

from truescope.route import app
