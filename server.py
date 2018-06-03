from flask import Flask, url_for, redirect, render_template, request, send_file
import db
from datetime import datetime
import os

app = Flask(__name__)


def createDateTime(ingresso):
    print(ingresso)
    anno, mese, giorno = ingresso.split("-", 2)
    data = datetime(int(anno), int(mese), int(giorno))
    return data


@app.errorhandler(400)
def page_400(_):
    return render_template('400.htm')


@app.errorhandler(404)
def page_404(_):
    return render_template('404.htm')


@app.errorhandler(500)
def page_500(_):
    return render_template('500.htm')


@app.route("/")
def page_root():
    return redirect(url_for('page_dashboard'))


@app.route("/misurazione")
def page_dashboard():
    session = db.Session()
    registrazioni = session.query(db.Registrazione).order_by(db.Registrazione.orario.desc()).limit(50).all()
    session.close()
    return render_template("dashboard.htm", registrazioni=registrazioni)


@app.route("/downloadCSV", methods=["POST"])
def page_downloadCSV():
    session = db.Session()
    margine1 = createDateTime(request.form["data1"])
    margine2 = createDateTime(request.form["data2"])
    risultati = session.query(db.Registrazione).filter(db.and_(
        db.Registrazione.orario >= margine1, db.Registrazione.orario <= margine2)).all()
    session.close()
    csv = open("risultato.csv", mode="w")
    csv.write("VALORE;DATA\n")
    for risultato in risultati:
        stringa = str(risultato.valore*0.01241) + ";" + str(risultato.orario) + "\n"
        csv.write(stringa)
    csv.close()
    return send_file('risultato.csv',
                     mimetype='text/csv',
                     attachment_filename='risultato.csv',
                     as_attachment=True)


@app.route("/average", methods=["POST"])
def page_average():
    session = db.Session()
    margine1 = createDateTime(request.form["data1"])
    margine2 = createDateTime(request.form["data2"])
    risultati = session.query(db.Registrazione).filter(db.and_(
        db.Registrazione.orario >= margine1, db.Registrazione.orario <= margine2)).all()
    session.close()
    media = 0.0
    divisori = len(risultati)
    for risultato in risultati:
        media += risultato.valore
    media = media / divisori
    media = media*0.01241
    return render_template("media.htm", media=media)


@app.route("/ricerca", methods=["POST"])
def page_ricerca():
    session = db.Session()
    margine1 = createDateTime(request.form["data5"])
    margine2 = createDateTime(request.form["data6"])
    risultati = session.query(db.Registrazione).filter(db.and_(
        db.Registrazione.orario >= margine1, db.Registrazione.orario <= margine2)).all()
    session.close()
    return render_template("dashboard.htm", registrazioni=risultati, alternativa=True)


@app.route("/misufake")
def page_misufake():
    session = db.Session()
    nuovamisu = session.query(db.Registrazione).filter_by(orario=datetime.now(), valore=10.2)
    session.add(nuovamisu)
    session.commit()
    session.close()
    return "OK"


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False)
