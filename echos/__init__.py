from flask import Flask
from flask_sqlalchemy import *
from flask_login import LoginManager


#initializing the webapp
app = Flask(__name__)

#setting up native flask-login manager
login_manager = LoginManager()
login_manager.init_app(app)

#setting secret key
app.config['SECRET_KEY']="AS7wvAhaKu4yFyVuPaTasCUDY6mg8c3RmjMFAAtQCfAxrUZxt5xZbTbVy8rHYagkAYG52jr\
                          VSz6aMBDPQt6bVLnPzd7ZBbCwAZnazwKkuYNvnKMVSqppmnvSV8xrwJZMXhPdQY6bhgHUjx\
                          x3cwHZkB66v4uYZWmdBNaLuDrnFZFgJS58KnSnPuQa2zQYjzqCZEZzz3gscmZvNCfhaRSFa\
                          M4AKu2UaHcW9K9Cqnf5pFLvBPTFmbAJCsuVEHPvKNSL"

#settig flask-sqalchemy database connection
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://echos:EchosApp@139.177.180.60/echos"
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

