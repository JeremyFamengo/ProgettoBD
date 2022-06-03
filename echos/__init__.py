from flask import Flask
from requests import Session
from sqlalchemy import *
from flask_sqlalchemy import *
from flask_login import LoginManager
from echos.config import config
from sqlalchemy.orm import sessionmaker


#initializing the webapp
app = Flask(__name__, static_folder=None)

#setting up native flask-login manager
login_manager = LoginManager()
login_manager.init_app(app)

#setting secret key
app.config['SECRET_KEY']= config.get('SECRET_KEY')

#settig flask-sqalchemy database connection
app.config['SQLALCHEMY_DATABASE_URI'] = config.get('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#setting sqlalchemy connection
engine_admin = create_engine(config.get('ADMIN_DB'), echo = True)
engine_user = create_engine(config.get('USER_DB'), echo = True)
engine_artist = create_engine(config.get('ARTIST_DB'), echo = True)
engine_home = create_engine(config.get('HOME_DB'), echo = True)

#genero le sessioni per ogni ruolo
Session = sessionmaker(bind = engine_admin)
Session_admin = Session()
Session = sessionmaker(bind = engine_user)
Session_user = Session()
Session = sessionmaker(bind = engine_artist)
Session_artist = Session()
Session = sessionmaker(bind = engine_home)
Session_home = Session()

# setting flask max dimensions of uploaded files to prevent crash and errors
app.config['MAX_CONTENT_PATH'] = 10485760

#setting upload folder
app.config['UPLOAD_FOLDER'] = "/tmp/"

from echos.models import User

login_manager.login_view = 'home_bp.login'

@login_manager.user_loader
#user loader
def load_user(id):
    user = Session_user.query(User).filter(User.id == id).first()
    return user
with app.app_context():
    # Import parts of our application
    from .home import routes
    from .admin import routes
    from .user import routes
    from .artist import routes

    # Register Blueprints
    app.register_blueprint(home.routes.home_bp)
    app.register_blueprint(admin.routes.admin_bp)
    app.register_blueprint(user.routes.user_bp)
    app.register_blueprint(artist.routes.artist_bp)