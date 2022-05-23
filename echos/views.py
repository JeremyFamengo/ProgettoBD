from flask import *
from flask_sqlalchemy import *
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash
from datetime import date

from echos import app
from echos.models import *
from echos.functions import *


# Funzione dedicata alla pagina principale del sito
@app.route('/')
def home():
    artisti = Top_five_artists_view.query.all()
    canzoni_recenti = Canzoni_recenti_view.query.all()
    canzoni_popolari = Canzoni_popolari_view.query.all()


    return render_template("index.html", artisti = artisti, canzoni = canzoni_recenti, popolari = canzoni_popolari)

# Funzione dedicata alla pagina di accesso al sito
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(mail=form.email.data).first()
        if user:
            if user.verify_password(form.psw.data):
                login_user(user)
                return redirect(url_for('profile'))
            else:
                print('Wrong password')
                flash('Wrong password')
        else:
            print('User does not exist')
            flash('User does not exist')

    return render_template("login.html", form=form)

# Funzione dedicata all'utente, dove vengono mostrate le canzoni più ascoltate, i generi più ascoltati e gli artisti più ascoltati
@app.route('/profile')
@login_required
def profile():
    dati = []
    statistiche = Statistiche_utente_view.query.filter_by(id_utente = current_user.id).all()
    
    if statistiche:
        dati = statistiche_utente(statistiche)
    else:
        dati = None

    return render_template("profile.html", user=current_user.username, dati = dati)

# Funzione dedicata onorevolmente alla pagina dei logo creatori
@app.route('/info')
def info():
    return render_template("info.html")

# Funzione dedicata al logout dell'utente
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Funzione dedicata alla registrazione dell'utente
@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User.query.filter_by(mail=form.email.data).first()
        if user is None:
            user = User(nome=form.nome.data, cognome=form.cognome.data, mail=form.email.data, psw=form.psw.data, data_di_nascita=form.data_di_nascita.data, id_artista=None, premium=False, ascoltate=[], username = form.username.data)
            user.debug()
            db.session.add(user)
            db.session.commit()

            print("User added correctly!")
            flash("User added correctly!")

            form.nome.data = ''
            form.cognome.data = ''
            form.email.data = ''
            form.username.data = ''
            form.psw.data = ''
            form.data_di_nascita.data = ''

            return redirect(url_for('login'))

        else:
            print("User already registered!")
            flash("User already registered!")
            form.psw.data = ''
            form.psw2.data = ''

    return render_template("register.html", form = form)

# Funzione dedicata alla gestione dei dati dell'utente
@app.route('/profileinfo', methods=['GET', 'POST'])
@login_required
def profileinfo():
    form = ModifyInfo()
    form2 = ModifyPsw()

    if form.submit1.data and form.validate():
        print("Modified info")
        user = User.query.filter_by(id = current_user.id).first()

        user.nome = form.nome.data
        user.cognome = form.cognome.data
        user.mail = form.email.data
        user.data_di_nascita = form.data_di_nascita.data

        db.session.commit()

        flash("Info updated correctly")


    if form2.submit2.data and form2.validate():
        user = User.query.filter_by(id = current_user.id).first()

        if user.verify_password(form2.old_psw.data):
            user.psw = generate_password_hash(form2.psw.data)
            print("Modified password")
            db.session.commit()
            flash("Modified password")
        else:
            print("wrong old password")
            flash("Insert your current password correctly")

    form.nome.data = current_user.nome
    form.cognome.data = current_user.cognome
    form.email.data = current_user.mail
    form.data_di_nascita.data = current_user.data_di_nascita

    
    if request.method == 'POST':
        delete_user = bool(int(request.form.get('delete_user')))
        id = request.form.get('id')

        if delete_user:
            Artista.query.filter_by(id_utente = id).update(dict(id_utente=0))
            User.query.filter_by(id = id).delete()
            db.session.commit()

        return redirect(url_for('login'))

    return render_template('profileinfo.html', form = form, form2 = form2, id_utente = current_user.id)


# Funzione dedicato agli utenti che non sono artisti.
# Permette ad un utente di inviare una richiesta all'amministratore per poter diventare una artista
@app.route('/artist', methods=['GET', 'POST'])
@login_required
def artist():
    form = ArtistForm()
    request_status = None
    nome_arte = None

    # controllo se esiste già una entry nella tabella artisti legata all'utente corrente e setto artist a True se vero, altrimenti a False
    artist = current_user.id_artista
    if artist:
        return redirect("/artist/dashboard")
    else:
        artist = False


    # controllo se esiste già una richiesta a nome dell'utente, se esiste prendo il codice si stato, altrimenti setto il codice di stato a 0
    if not artist:
        request = Richieste_diventa_artista.query.filter_by(id_utente = current_user.id).first()
        if request:
            request_status = request.stato_richiesta
        else:
            request_status = 0

        if form.validate_on_submit():
            nome_arte = form.nome_arte.data
            motivazione = form.motivazione.data
            stato_richiesta = 1
            id_utente = current_user.id

            richiesta = Richieste_diventa_artista(nome_arte, motivazione, stato_richiesta, id_utente)
            richiesta.debug()
            db.session.add(richiesta)
            db.session.commit()

            form.nome_arte.data = ''
            form.motivazione.data = ''

            return redirect('profile')

    return render_template('artist.html', form = form, artist = artist, nome_arte = nome_arte, request_status = request_status)

# Funzione dedidicata alla pagina dell'amministratore
@app.route('/admin', methods=['GET', 'POST'])
@requires_auth
def admin():

    if request.method == 'POST':
        id = request.form['id_utente']
        nome_arte = request.form['nome_arte']
        print(id)
        print(nome_arte)

        accept = bool(request.form['accept'])
        print(accept)


        # TODO: controllare ridondanze in questa procedura
        if accept:
            req = Richieste_diventa_artista.query.filter_by(id_utente = id).first()
            req.stato_richiesta = 2
            artista = Artista(nome_arte, date.today(), id)
            db.session.add(artista)
            db.session.commit()

            user = User.query.filter_by(id = id).first()
            artista = Artista.query.filter_by(id_utente = user.id).first()
            user.id_artista = artista.id_artista

            db.session.commit()

        else:
            req = Richieste_diventa_artista.query.filter_by(id_utente = id).first()
            req.stato_richiesta = -1
            db.session.commit()

    requests = Richieste_diventa_artista.query.filter_by(stato_richiesta = '1').all()
    return render_template("admin.html", requests = requests)

# Funzione dedicata alla dashboard degli artisti
@app.route('/artist/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if current_user.id_artista == None:
        flash("You must be an Artist to access the artist's dashboard")
        return redirect('/profile')

    user = Artista.query.filter_by(id_artista = current_user.id_artista).first()
    songs = Canzoni.query.filter_by(id_artista = current_user.id_artista)
    albums = Album.query.filter_by(id_artista = user.id_artista).all()
    length = len(albums)

    if request.method == 'POST':
        id = request.form.get('id')
        print(id)
        Canzoni.query.filter_by(id=id).delete()
        db.session.commit()

    return render_template("dashboard.html", user=user.nome_arte, albums=albums, songs=songs, length = length)

# Funzione dedicata alla maschera d'inserimento della canzone
@app.route('/artist/uploadsong')
@login_required
def uploadsong():
    if current_user.id_artista == None:
        flash("You must be an Artist to access the artist's dashboard")
        return redirect('/profile')

    form = UploadForm()

    artista = Artista.query.filter_by(id_artista = current_user.id_artista).first()
    generi = Generi_Musicali.query.all()
    albums = Album_artisti_view.query.filter_by(id_artista = artista.id_artista).all()


    choices = []
    for album in albums:
        is_empty = album.vuoto
        if album.singolo and is_empty:
            tmp = (album.id_album,album.titolo)
            choices.append(tmp)
        elif not album.singolo:
            tmp = (album.id_album,album.titolo)
            choices.append(tmp)

    form.album.choices = choices

    choices = []
    for genere in generi:
        tmp = (genere.id_genere,genere.nome)
        choices.append(tmp)

    form.genere.choices = choices

    return render_template("uploadsong.html", form=form)

# Funzione dedicata alle statistiche
@app.route('/artist/statistiche')
@login_required
def statistiche():
    if current_user.id_artista == None:
        flash("You must be an Artist to access the artist's dashboard")
        return redirect('/profile')


    n_riproduzioni_album_canzoni = N_riproduzioni_album_canzoni_view.query.filter_by(id_artista = current_user.id_artista).all()

    temp = []
    ids = []
    for ele in n_riproduzioni_album_canzoni:
        ids.append(ele.titolo_album)
    ids = set(ids)

    for id in ids:
        temp2 = []
        for ele in n_riproduzioni_album_canzoni:
            if ele.titolo_album == id:
                temp2.append(ele)
        temp.append(temp2)

    return render_template("statistiche.html",canzoniPerAlbum=temp)

# Funzione dedicata alla creaizone di un album
@app.route('/artist/creaalbum', methods=['GET', 'POST'])
@login_required
def creaalbum():
    if current_user.id_artista == None:
        flash("You must be an Artist to access the artist's dashboard")
        return redirect('/profile')

    artista = Artista.query.filter_by(id_artista = current_user.id_artista).first()

    form = CreateAlbumForm()


    if form.is_submitted():
        titolo = form.titolo.data
        anno = form.anno.data
        singolo = bool(int(form.singolo.data))
        restricted = bool(int(form.restricted.data))
        scadenza = form.scadenza.data

        album = Album(artista.id_artista, singolo, scadenza, restricted, titolo, anno)

        album.debug()

        db.session.add(album)
        db.session.commit()

        form.titolo.data = ''
        form.scadenza.data = ''
        form.anno.data = ''
        form.singolo.data = ''
        form.restricted.data = ''

        flash("Album aggiunto correttamente")

    return render_template("creaalbum.html", form=form)

# Funzione dedicata all'inserimento di una nuova canzone
@app.route('/168AN4df15/uploader', methods=['GET', 'POST'])
@login_required
def uploader():

    form = UploadForm()

    if form.is_submitted():
        f = request.files['file']
        titolo = form.titolo.data
        data_uscita = form.data_uscita.data
        riservato = bool(int(form.riservato.data))
        id_album = int(form.album.data)
        scadenza = form.scadenza.data
        genere=form.genere.data
        id_artista = current_user.id_artista
        data = f.stream.read()
        durata = 180
        n_riproduzioni=0


        canzone = Canzoni(id_artista=id_artista, titolo=titolo, scadenza=scadenza, data_inserimento=date.today(), data_uscita=data_uscita, id_genere=genere, file=data, riservato=riservato, extension='mp3', durata=durata, n_riproduzioni=n_riproduzioni)

        db.session.add(canzone)

        id_canzone = Canzoni.query.filter_by(id_artista = current_user.id_artista, data_uscita = data_uscita).first().id

        addToAlbum(id_album,id_canzone)

        flash("file uploaded successfully")

    return redirect('/artist/uploadsong')

# Funzione dedicata alla pagina che mostra i metadati di una singola canzone
@app.route('/player')
@login_required
def player():

    id = request.args.get('id')
    canzone = Canzoni.query.filter_by(id = id).first()

    # Aggironamento numero di riproduzioni svolte in questa canzone

    artista = Artista.query.filter_by(id_artista = canzone.id_artista).first()
    genere = Generi_Musicali.query.filter_by(id_genere = canzone.id_genere).first()
    descrizione = genere.descrizione
    genere = genere.nome

    if artista.id_artista != current_user.id_artista:
        nPlayTMP=Canzoni.n_riproduzioni+1
        Canzoni.query.filter_by(id = id).update(dict(n_riproduzioni=nPlayTMP))
        db.session.commit()

        ascolto = Utenti_ascolti(current_user.id, canzone.id, 1)
        db.session.add(ascolto)
        db.session.commit()

    artista = artista.nome_arte

    riservato = canzone.riservato
    print(current_user.premium)
    print(riservato)
    if current_user.premium:
        riservato = False
    print(riservato)


    return render_template("player.html", canzone=canzone, artista=artista, riservato=riservato, genere=genere, descrizione=descrizione)

# Funzione dedicata alla creazione di una playlist
@app.route('/creaplaylist', methods=['GET', 'POST'])
@login_required
def creaplaylist():
    form = CreaPlaylistForm()

    if form.validate_on_submit():
        titolo = form.titolo.data
        restricted = bool(int(form.restricted.data))
        id_utente = current_user.id

        playlist = Playlist(titolo = titolo, id_utente = id_utente, restricted = restricted)
        print(playlist)

        db.session.add(playlist)
        db.session.commit()

        flash("Playlist creata correttamente")

        return redirect("/playlist")

    return render_template("creaplaylist.html", form = form)

# Funzione dedicata alla pagina playlist
@app.route('/playlist', methods=['GET', 'POST'])
@login_required
def playlist():


    if request.method == 'POST':
        is_song = bool(int(request.form.get('delete_song')))
        id = request.form.get('id')

        if is_song:
            Canzoni.query.filter_by(id = id).delete()
            db.session.commit()
        else:
            Playlist.query.filter_by(id_playlist = id).delete()
            db.session.commit()


    playlists = Playlist_canzoni_view.query.filter_by(id_utente=current_user.id).all()

    temp = []
    ids = []
    for playlist in playlists:
        ids.append(playlist.id_playlist)
    ids = set(ids)

    for id in ids:
        temp2 = []
        for playlist in playlists:
            if playlist.id_playlist == id:
                temp2.append(playlist)
        temp.append(temp2)

    return render_template("playlist.html", playlists = temp)

# Funzione dedicata al tasto cerca
@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():

    resultQuery=getSearchTable()

    playlists = Playlist.query.filter_by(id_utente = current_user.id).all()
    count = len(resultQuery)

    if request.method == 'POST':
        id_playlist = request.form['id_playlist']
        id_canzone = request.form['id_canzone']
        addToPlaylist(id_playlist, id_canzone)

    return render_template("search.html", songs = resultQuery, count_canzoni = count, playlists = playlists)

# Funzione che richiama la pagina di errore 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')


# Funzione dedicata alla visita di un album specifico
@app.route('/canzonialbum', methods=['GET', 'POST'])
@login_required
def canzonialbum():
    if request.method == 'POST':
        is_song = bool(int(request.form.get('delete_song')))
        id = request.form.get('id')
    
        if is_song:
            Canzoni.query.filter_by(id = id).delete()
            db.session.commit()
        else:
            Album.query.filter_by(id_album = id).delete()
            db.session.commit()
            return redirect('/artist/dashboard')
        
        return redirect("/canzonialbum")

    id_album = request.args.get('id_album')

    album_titolo = Album.query.filter_by(id_album = id_album).first().titolo
    songs = Album_canzoni_view.query.filter_by(id_album = id_album).all()

    return render_template("/canzonialbum.html" , songs = songs, titolo = album_titolo, id_album = id_album)