from echos import *
from echos.models import *
from echos.functions import *
from flask_login import *
from flask import current_app as app

# Blueprint Configuration
user_bp = Blueprint(
    'user_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

# Funzione dedicata all'utente, dove vengono mostrate le canzoni più ascoltate, i generi più ascoltati 
# e gli artisti più ascoltati
@user_bp.route('/profile')
@login_required
def profile():
    dati = []
    statistiche = Session_user.query(Statistiche_utente_view).filter(Statistiche_utente_view.id_utente == current_user.id).all()
    
    if statistiche:
        dati = statistiche_utente(statistiche)
    else:
        dati = None

    return render_template("profile.html", user=current_user.username, dati = dati)

# Funzione dedicata al logout dell'utente
@user_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Funzione dedicata alla registrazione dell'utente
@user_bp.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = Session_user.query(User).filter(User.mail == form.email.data).first()
        if user is None:
            user = User(nome=form.nome.data, cognome=form.cognome.data, mail=form.email.data, 
                        psw=form.psw.data, data_di_nascita=form.data_di_nascita.data, id_artista=None,
                        premium=False, ascoltate=[], username = form.username.data)
            user.debug()
            Session_user.add(user)
            Session_user.commit()

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
@user_bp.route('/profileinfo', methods=['GET', 'POST'])
@login_required
def profileinfo():
    form = ModifyInfo()
    form2 = ModifyPsw()

    if form.submit1.data and form.validate():
        print("Modified info")
        user = Session_user.query(User).filter(User.id == current_user.id).first()

        user.nome = form.nome.data
        user.cognome = form.cognome.data
        user.mail = form.email.data
        user.data_di_nascita = form.data_di_nascita.data

        Session_user.commit()

        flash("Info updated correctly")


    if form2.submit2.data and form2.validate():
        user = Session_user.query(User).filter(User.id == current_user.id).first()

        if user.verify_password(form2.old_psw.data):
            user.psw = generate_password_hash(form2.psw.data)
            print("Modified password")
            Session_user.commit()
            flash("Modified password")
        else:
            print("wrong old password")
            flash("Insert your current password correctly")

    form.nome.data = current_user.nome
    form.cognome.data = current_user.cognome
    form.email.data = current_user.mail
    form.data_di_nascita.data = current_user.data_di_nascita

    
    if request.method == 'POST' and (request.form.get('delete_user')!=None):
        delete_user = bool(int(request.form.get('delete_user')))
        id = request.form.get('id')

        if delete_user:
            Session_user.query(Artista).filter(Artista.id_utente == id).update({'id_utente':0})
            Session_user.query(User).filter(User.id == id).delete()
            Session_user.commit()

        return redirect(url_for('login'))

    return render_template('profileinfo.html', form = form, form2 = form2, id_utente = current_user.id)

# Funzione dedicata alla pagina che mostra i metadati di una singola canzone
@user_bp.route('/player')
@login_required
def player():

    id = request.args.get('id')
    canzone = Session_user.query(Canzoni).filter(Canzoni.id == id).one()

    # Aggironamento numero di riproduzioni svolte in questa canzone

    artista = Session_user.query(Artista).filter(Artista.id_artista == canzone.id_artista).one()
    genere = Session_user.query(Generi_Musicali).filter(Generi_Musicali.id_genere == canzone.id_genere).one()
    descrizione = genere.descrizione
    genere = genere.nome

    if artista.id_artista != current_user.id_artista:
        nPlayTMP=Canzoni.n_riproduzioni+1
        Session_user.query(Canzoni).filter(Canzoni.id == id).update({'n_riproduzioni':nPlayTMP})
        Session_user.commit()

        ascolto = Utenti_ascolti(current_user.id, canzone.id, 1)
        Session_user.add(ascolto)
        Session_user.commit()

    artista = artista.nome_arte

    riservato = canzone.riservato
    print(current_user.premium)
    print(riservato)
    if current_user.premium:
        riservato = False
    print(riservato)


    return render_template("player.html", canzone=canzone, artista=artista, riservato=riservato, genere=genere,
                            descrizione=descrizione)


# Funzione dedicata alla creazione di una playlist
@user_bp.route('/creaplaylist', methods=['GET', 'POST'])
@login_required
def creaplaylist():
    form = CreaPlaylistForm()

    if form.validate_on_submit():
        titolo = form.titolo.data
        restricted = bool(int(form.restricted.data))
        id_utente = current_user.id

        playlist = Playlist(titolo = titolo, id_utente = id_utente, restricted = restricted)
        print(playlist)

        Session_user.add(playlist)
        Session_user.commit()

        flash("Playlist creata correttamente")

        return redirect("/playlist")

    return render_template("creaplaylist.html", form = form)

# Funzione dedicata alla pagina playlist
@user_bp.route('/playlist', methods=['GET', 'POST'])
@login_required
def playlist():


    if request.method == 'POST':
        is_song = bool(int(request.form.get('delete_song')))
        id = request.form.get('id')
        id_playlist = request.form.get('id_playlist')

        if is_song:
            Session_user.query(Playlist_canzoni).filter(Playlist_canzoni.id_canzone == id, Playlist_canzoni.id_playlist == id_playlist).delete()
            Session_user.commit()
        else:
            Session_user.query(Playlist).filter(Playlist.id_playlist == id).delete()
            Session_user.commit()


    playlists = Session_user.query(Playlist_canzoni_view).filter(Playlist_canzoni_view.id_utente==current_user.id).all()

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
