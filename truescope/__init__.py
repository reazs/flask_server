from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_admin import Admin
from flask_msearch import Search

app = Flask(__name__)

CORS(app)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['postgres://tcezfvpubcnejt:adbd753a64fdf7f3797530f681f7da05b4e9354e30fd231382c9bd3eb1573cc3@ec2-44-199-22-207.compute-1.amazonaws.com:5432/d4jum54hsrqhfaPS F:\web_development\flask_ptyhon\truescope\flask_server']= 'sqlite:///data.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://qzhcvvkcvrcboz:a1ad05e1d1675a07058d26951da68e0109d964ffc2ae5f8cc9e77a1a1df671e0@ec2-'
'44-193-178-122.compute-1.amazonaws.com:5432/d1fdu8dfhb60v4'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "sadjfkadfa09234"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
search = Search()
search.init_app(app)
admin = Admin(app)
login_manager = LoginManager(app)
login_manager.login_view = "access_denied"
login_manager.login_message = "Access Denied!"

from truescope.route import app
