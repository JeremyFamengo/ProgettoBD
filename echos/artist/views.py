from echos import *
from echos.models import *
from flask_login import *
from datetime import date
from echos.functions import *

# Funzione dedicata alla dashboard degli artisti
@app.route('/artist/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if current_user.id_artista == None:
        flash("You must be an Artist to access the artist's dashboard")
        return redirect('/profile')

    user = Session_artist.query(Artista).filter(Artista.id_artista == current_user.id_artista).one()
    songs = Session_artist.query(Canzoni).filter(Canzoni.id_artista == current_user.id_artista).all()
    albums = Session_artist.query(Album).filter(Album.id_artista == user.id_artista).all()
    length = len(albums)

    if request.method == 'POST':
        delete_song = request.form.get('id')
        if delete_song:
            Session_artist.query(Canzoni).filter(Canzoni.id==delete_song).delete()
            Session_artist.commit()
            return redirect('/artist/dashboard')
        
        delete_artista = bool(int(request.form.get('delete_artista')))
        if delete_artista: 
            Session_artist.query(Artista).filter(Artista.id_artista == user.id_artista).delete()
            Session_artist.commit() 
            return redirect('/profile')

    return render_template("dashboard.html", user=user.nome_arte, albums=albums, songs=songs, length = length)

# Funzione dedicata alla maschera d'inserimento della canzone
@app.route('/artist/uploadsong')
@login_required
def uploadsong():
    if current_user.id_artista == None:
        flash("You must be an Artist to access the artist's dashboard")
        return redirect('/profile')

    form = UploadForm()

    artista = Session_artist.query(Artista).filter(Artista.id_artista == current_user.id_artista).one()
    generi = Session_artist.query(Generi_Musicali).all()
    albums = Session_artist.query(Album_artisti_view).filter(Album_artisti_view.id_artista == artista.id_artista).all()


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


    n_riproduzioni_album_canzoni = Session_artist.query(N_riproduzioni_album_canzoni_view).filter\
                                    (N_riproduzioni_album_canzoni_view.id_artista == current_user.id_artista).all()

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

    artista = Session_artist.query(Artista).filter(Artista.id_artista == current_user.id_artista).one()

    form = CreateAlbumForm()


    if form.is_submitted():
        titolo = form.titolo.data
        anno = form.anno.data
        singolo = bool(int(form.singolo.data))
        restricted = bool(int(form.restricted.data))
        scadenza = form.scadenza.data

        album = Album(artista.id_artista, singolo, scadenza, restricted, titolo, anno)

        album.debug()

        Session_artist.add(album)
        Session_artist.commit()

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


        canzone = Canzoni(id_artista=id_artista, titolo=titolo, scadenza=scadenza, data_inserimento=date.today(),
                          data_uscita=data_uscita, id_genere=genere, file=data, riservato=riservato, extension='mp3',
                          durata=durata, n_riproduzioni=n_riproduzioni)

        Session_artist.add(canzone)
        Session_artist.commit()

        id_canzone = Session_artist.query(Canzoni).filter(Canzoni.id_artista == current_user.id_artista, Canzoni.data_uscita == data_uscita).one().id

        addToAlbum(id_album,id_canzone)

        flash("file uploaded successfully")

    return redirect('/artist/uploadsong')


# Funzione dedicata alla visita di un album specifico
@app.route('/canzonialbum', methods=['GET', 'POST'])
@login_required
def canzonialbum():
    if request.method == 'POST':
        is_song = bool(int(request.form.get('delete_song')))
        id = request.form.get('id')
        id_album = request.form.get('id_album')
    
        if is_song:
            Session_artist.query(Canzoni).filter(Canzoni.id == id).delete()
            Session_artist.commit()
        else:
            Session_artist.query(Album).filter(Album.id_album == id_album).delete()
            Session_artist.commit()
            return redirect('/artist/dashboard')
        
        return redirect("/canzonialbum?id_album=" + str(id_album))

    id_album = request.args.get('id_album')

    album_titolo = Session_artist.query(Album).filter(Album.id_album == id_album).first().titolo
    songs = Session_artist.query(Album_canzoni_view).filter(Album_canzoni_view.id_album == id_album).all()

    return render_template("/canzonialbum.html" , songs = songs, titolo = album_titolo, id_album = id_album)