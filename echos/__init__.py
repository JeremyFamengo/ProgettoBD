from flask import Flask
from flask_sqlalchemy import *
from flask_login import LoginManager
from echos.config import config


#initializing the webapp
app = Flask(__name__)

#setting up native flask-login manager
login_manager = LoginManager()
login_manager.init_app(app)

#setting secret key
app.config['SECRET_KEY']= config.get('SECRET_KEY')

#settig flask-sqalchemy database connection
app.config['SQLALCHEMY_DATABASE_URI'] = config.get('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# setting flask max dimensions of uploaded files to prevent crash and errors
app.config['MAX_CONTENT_PATH'] = 10485760

#setting upload folder
app.config['UPLOAD_FOLDER'] = "/tmp/"

#initializing database with flask-sqalchemy
db = SQLAlchemy(app)

import echos.views


from echos.models import User

login_manager.login_view = 'login'

@login_manager.user_loader
#user loader
def load_user(id):
    return User.query.get(id)

