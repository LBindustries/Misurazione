from flask import Flask, url_for, redirect, render_template
import db
from datetime import datetime
import os

app = Flask(__name__)


@app.route("/")
def page_root():
    return redirect(url_for('page_dashboard'))


@app.route("/misurazione")
def page_dashboard():
    session = db.Session()
    registrazioni = session.query(db.Registrazione).order_by(db.Registrazione.orario.desc()).limit(50).all()
    session.close()
    return render_template("dashboard.htm", registrazioni=registrazioni)


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
