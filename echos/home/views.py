from flask import Blueprint, render_template
from echos import *
from echos.models import *

home = Blueprint('home', __name__, template_folder="templates")

# Funzione dedicata alla pagina principale del sito
@home.route('/')
def home():
    artisti = Session_home.query(Top_five_artists_view).all()
    canzoni_recenti =  Session_home.query(Canzoni_recenti_view).all()
    canzoni_popolari =  Session_home.query(Canzoni_popolari_view).all()

    return render_template("index.html", artisti = artisti, canzoni = canzoni_recenti, popolari = canzoni_popolari)