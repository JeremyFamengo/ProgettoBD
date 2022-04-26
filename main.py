from flask import *
from flask_sqlalchemy import *
from flask_login import UserMixin, current_user, login_user, LoginManager, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField
from wtforms.validators import DataRequired, EqualTo


#######################################################
# CONFIGS
#######################################################

#initializing the webapp
app = Flask(__name__)

#setting secret key
app.config['SECRET_KEY']="AS7wvAhaKu4yFyVuPaTasCUDY6mg8c3RmjMFAAtQCfAxrUZxt5xZbTbVy8rHYagkAYG52jrVSz6aMBDPQt6bVLnPzd7ZBbCwAZnazwKkuYNvnKMVSqppmnvSV8xrwJZMXhPdQY6bhgHUjxx3cwHZkB66v4uYZWmdBNaLuDrnFZFgJS58KnSnPuQa2zQYjzqCZEZzz3gscmZvNCfhaRSFaM4AKu2UaHcW9K9Cqnf5pFLvBPTFmbAJCsuVEHPvKNSL"

#settig flask-sqalchemy database connection
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://echos:EchosApp@139.162.163.103/echos"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#initializing database with flask-sqalchemy
db = SQLAlchemy(app)

#setting up native flask-login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


#######################################################
# CLASSES
#######################################################

#class that defines a user in the table of Utenti in the database
class User(db.Model, UserMixin):
    __tablename__ = "utenti"
    nome  = db.Column(db.String(20))
    cognome = db.Column(db.String(20))
    mail = db.Column(db.String(40), unique=True)
    cf = db.Column(db.String, primary_key=True)
    data_di_nascita = db.Column(db.Date)
    id_artista = db.Column(db.String(30))
    
    psw = db.Column(db.String(128))

    def __init__(self, nome, cognome, mail, cf, psw, data_di_nascita, id_artista):
        self.nome = nome
        self.cognome = cognome
        self.mail = mail
        self.cf = cf
        self.psw = generate_password_hash(psw, "sha256")
        self.data_di_nascita = data_di_nascita
        self.id_artista = id_artista

    def verify_password(self, psw):
        return check_password_hash(self.psw, psw)

    def debug(self):
        print("\n---------[DEBUG]---------\n")
        print(self.nome)
        print(self.cognome)
        print(self.mail)
        print(self.cf)
        print(self.psw)
        print(self.data_di_nascita)
        print(self.id_artista)
        print("\n-------------------------\n")
    
    def get_id(self):
        return self.cf

#class that defines the login form
class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    psw = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")

#class that defines the register form
class RegisterForm(FlaskForm):
    nome = StringField("Nome*", validators=[DataRequired()])
    cognome = StringField("Cognome*", validators=[DataRequired()])
    cf = StringField("CF*", validators=[DataRequired()])
    email = StringField("Email*", validators=[DataRequired()])
    psw = PasswordField("Password*", validators=[DataRequired(), EqualTo('psw2', message='Passwords do not match')])
    psw2 = PasswordField("Confirm Password*", validators=[DataRequired()])
    data_di_nascita = StringField("Data di nascita*", validators=[DataRequired()])
    submit = SubmitField("Register")

#######################################################
# ROUTES
#######################################################

#home
@app.route('/')
def home():
    return render_template("index.html")

#login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(mail=form.email.data).first()
        if user:
            if user.verify_password(form.psw.data):
                login_user(user)
                print('Login succesful')
                flash('Login succesful')
                return redirect(url_for('profile'))
            else:
                print('Wrong password')
                flash('Wrong password')
        else:
            print('User does not exist')
            flash('User does not exist')
                
    return render_template("login.html", form=form)

#profile page
@app.route('/profile')
@login_required
def profile():
    return render_template("profile.html", user=current_user.nome)

#info page
@app.route('/info')
def info():
    
    return render_template("info.html")

#logout function as route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

#register page and function
@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User.query.filter_by(cf=form.cf.data).first()
        if user is None:
            user = User(nome=form.nome.data, cognome=form.cognome.data, mail=form.email.data, cf=form.cf.data, psw=form.psw.data, data_di_nascita=form.data_di_nascita.data, id_artista=None)
            user.debug()
            db.session.add(user)
            db.session.commit()
            print("User added correctly!")
            flash("User added correctly!")
            form.nome.data = ''
            form.cognome.data = ''
            form.email.data = ''
            form.cf.data = ''
            form.psw.data = ''
            form.data_di_nascita.data = ''
            
            return redirect(url_for('login'))

        else:
            print("User already registered!")
            flash("User already registered!")
            form.psw.data = ''
            form.psw2.data = ''

    return render_template("register.html", form = form)

@app.route('/test')
def test():
    return render_template('test.html')

#######################################################
# FUNCTIONS
#######################################################

@login_manager.user_loader
def load_user(cf):
    return User.query.get(cf)


if __name__ == "__main__":
    app.run(debug=True)