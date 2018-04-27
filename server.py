from flask import Flask, session, url_for, redirect, request, render_template, abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date, timedelta
import os
import threading

app = Flask(__name__)
app.secret_key = "dovreiesserenascosta"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Registrazione(db.Model):
    __tablename__ = "registrazione"
    rid = db.Column(db.Integer, primary_key=True)
    orario = db.Column(db.DateTime, nullable=False)
    valore = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return "{}/{}/{} {}:{} [{}]".format(self.orario.day, self.orario.month, self.year, self.hour, self.minute,
                                            self.valore)


@app.route("/")
def page_root():
    return redirect(url_for('page_dashboard'))


@app.route("/misurazione")
def page_dashboard():
    registrazioni = Registrazione.query.order_by(Registrazione.orario.desc()).limit(50).all()
    return render_template("dashboard.htm", registrazioni=registrazioni)


@app.route("/misufake")
def page_misufake():
    nuovamisu = Registrazione(orario=datetime.now(), valore=10.2)
    db.session.add(nuovamisu)
    db.session.commit()
    return "OK"


if __name__ == "__main__":
    # Se non esiste il database viene creato
    if not os.path.isfile("db.sqlite"):
        db.create_all()
    app.run(host="0.0.0.0", debug=False)
