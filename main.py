from crypt import methods
from flask import *

app = Flask(__name__)

# SQLite supporta database transienti in RAM (echo attiva il logging)

#TODO: oscuare credenziali portandole duore dalla cartella pubblica
#engine = create_engine('postgresql://postgres:trolese@localhost:5432/progetto', echo = True)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/profile')
def profile():
    return render_template("profile.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template("login.html")

@app.route('/info')
def info():
    return render_template("info.html")

if __name__ == "__main__":
    app.run(debug=True)