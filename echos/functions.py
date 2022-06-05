
from functools import wraps
from flask import request, Response
from echos.models import *
from echos import Session_artist, Session_user




# Aggiungo una canzone alla playlist
def addToPlaylist(id_playlist, id_canzone):

    playlist_canzoni=Playlist_canzoni(id_playlist,id_canzone)
    Session_user.add(playlist_canzoni)
    Session_user.commit()


# Aggiungo una canzone all'album
def addToAlbum(album_id, id_canzone):

    album_canzoni=Album_canzoni(album_id,id_canzone)
    Session_artist.add(album_canzoni)
    Session_artist.commit()

    return redirect('/search')

# funzione per elaborare l'array di dati relativi alle statistiche dell'utente
def statistiche_utente(statistiche):
    dati = []
    canzoni_piu_ascoltate = []
    generi_piu_ascoltati = []
    generi_consigliati = []
    artisti_piu_ascoltati = []
    canzoni_consigliate = [] #canzoni dei generi più ascoltati con più ascolti globali (fare una view)

    for s in statistiche:
        temp = [s.id_genere, s.nome_genere, 0]
        if temp not in generi_piu_ascoltati:
            generi_piu_ascoltati.append(temp)

    for s in statistiche:
        temp = [s.id_artista, s.nome_arte, 0]
        if temp not in artisti_piu_ascoltati:
            artisti_piu_ascoltati.append(temp)

    for s in statistiche:
        canzoni_piu_ascoltate.append((s.id_canzone, s.n_ascolti, s.titolo_canzone))
        for g in generi_piu_ascoltati:
            if s.id_genere == g[0]:
                g[2] = g[2] + s.n_ascolti

        for a in artisti_piu_ascoltati:
            if s.id_artista == a[0]:
                a[2] = a[2] + s.n_ascolti

    
    #sorting secondo certi parametri
    artisti_piu_ascoltati.sort(key = lambda x: x[2], reverse=True)
    generi_piu_ascoltati.sort(key = lambda x: x[2], reverse=True)
    canzoni_piu_ascoltate.sort(key = lambda x: x[1], reverse=True)
    
    
    
    if len(generi_piu_ascoltati) > 3:
        generi_consigliati = [generi_piu_ascoltati[0], generi_piu_ascoltati[1], generi_piu_ascoltati[3]]
    else:
        generi_consigliati = generi_piu_ascoltati

    dati = [canzoni_piu_ascoltate, generi_piu_ascoltati, generi_consigliati, artisti_piu_ascoltati, canzoni_consigliate]

    return dati

# semplice funzione per controllare la correttezza delle password
def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == 'admin' and password == 'Admin'

# Sends a 401 response that enables basic auth
def authenticate():
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

# decoratore per proteggere una pagina con le credenziali specificate in check_auth()
def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated