from crypt import methods
from flask import *
import os

app = Flask(__name__)

app.secret_key="AS7wvAhaKu4yFyVuPaTasCUDY6mg8c3RmjMFAAtQCfAxrUZxt5xZbTbVy8rHYagkAYG52jrVSz6aMBDPQt6bVLnPzd7ZBbCwAZnazwKkuYNvnKMVSqppmnvSV8xrwJZMXhPdQY6bhgHUjxx3cwHZkB66v4uYZWmdBNaLuDrnFZFgJS58KnSnPuQa2zQYjzqCZEZzz3gscmZvNCfhaRSFaM4AKu2UaHcW9K9Cqnf5pFLvBPTFmbAJCsuVEHPvKNSL"

# SQLite supporta database transienti in RAM (echo attiva il logging)

#TODO: oscuare credenziali portandole duore dalla cartella pubblica
#engine = create_engine('postgresql://postgres:trolese@localhost:5432/progetto', echo = True)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/profile')
def profile():
    if 'user' in session:
        user = session['user']
        return render_template("profile.html", user=user)
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['user']
        password = request.form['pass']
        if user != '' and password != '':
            session['user'] = user
            session['password'] = password
            return redirect(url_for('profile'))
        else:
            return render_template("login.html")
    else:
        return render_template("login.html")

@app.route('/info')
def info():
    return render_template("info.html")

@app.route('/logout')
def logout():
    session.pop('user')
    session.pop('password')

if __name__ == "__main__":
    app.run(debug=True)