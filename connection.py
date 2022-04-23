import sqlalchemy
from sqlalchemy import *
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for

app = Flask(__name__)

# SQLite supporta database transienti in RAM (echo attiva il logging)

#TODO: oscuare credenziali portandole duore dalla cartella pubblica
#engine = create_engine('postgresql://postgres:trolese@localhost:5432/progetto', echo = True)

@app.route('/')
def hello_world():
    return render_template('login.html')