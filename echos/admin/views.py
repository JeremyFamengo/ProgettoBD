from echos import *
from echos.models import *
from flask_login import *
from echos.functions import *
from datetime import date

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
            req = Session_admin.query(Richieste_diventa_artista).filter(Richieste_diventa_artista.id_utente == id).first()
            req.stato_richiesta = 2
            artista = Artista(nome_arte, date.today(), id)
            Session_admin.add(artista)
            Session_admin.commit()

            user = Session_admin.query(User).filter(User.id == id).one()
            artista = Session_admin.query(Artista).filter(Artista.id_utente == user.id).one()
            user.id_artista = artista.id_artista

            Session_admin.commit()

        else:
            req = Session_admin.query(Richieste_diventa_artista).filter(Richieste_diventa_artista.id_utente == id).first()
            req.stato_richiesta = -1
            Session_admin.commit()

    requests = Session_admin.query(Richieste_diventa_artista).filter(Richieste_diventa_artista.stato_richiesta == '1').all()
    return render_template("admin.html", requests = requests)

