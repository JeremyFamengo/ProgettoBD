from flask import *

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/profile')
def profile():
    return render_template("profile.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/info')
def info():
    return render_template("info.html")

if __name__ == "__main__":
    app.run(debug=True)