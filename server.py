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
    print(risultati)
    session.close()
    csv = open("risultato.csv", mode="w")
    csv.write("VALORE;DATA\n")
    for risultato in risultati:
        stringa = str(risultato.valore) + ";" + str(risultato.orario) + "\n"
        csv.write(stringa)
    csv.close()
    return send_file('risultato.csv',
              mimetype='text/csv',
              attachment_filename='risultato.csv',
              as_attachment=True)


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
