from ast import Pass
from crypt import methods
from email.policy import default
from enum import unique
from Repository.user import CreateUser
from flask import Flask, flash, session, render_template, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, IntegerField
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from datetime import datetime 
from flask_migrate import Migrate

User = CreateUser("Sara", "Jones", "sara.jones@gmail.com", "SaraJones", "MojaLozinka12345")

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/biljke.sqlite'
app.config['SECRET_KEY'] = 'tajni_kljuc'

moment = Moment(app) #izradimo objek iz ove klase, objek koj ce nam omogucit azuriranje baze podataka, predamu mu app
db = SQLAlchemy(app)
migrate = Migrate(app,db)


#region Class

class Biljke (db.Model):
    __tablename__ = 'Biljke'
    id = db.Column(db.Integer(), primary_key = True )
    ime_biljke = db.Column(db.String(50), unique = True , nullable = False)
    slika = db.Column (db.String(), nullable = False, default = 'default.jpg')
    max_svjetlost = db.Column (db.Float(), nullable = False )
    min_svjetlost = db.Column (db.Float(), nullable = False)
    max_ph = db.Column (db.Integer(), nullable = False)
    min_ph = db.Column (db.Integer(), nullable = False)
    max_vlaznost = db.Column (db.Integer(), nullable = False)
    min_vlaznost = db.Column (db.Integer(), nullable = False)
    max_temp = db.Column (db.Float(), nullable = False)
    min_temp = db.Column (db.Float(), nullable = False)
    vaze = db.relationship('Vaze', backref = 'biljka', lazy = True) #backref kreira column u drugoj tabeli sa kojom spajamo ovu tabelu, One to many relationship


class Form_za_biljke (FlaskForm):
    ime_biljke = StringField('Ime Biljke')
    slika = StringField('Dodaj fotografiju') #kako dodam fotografij??
    max_svjetlost = FloatField('Maximalna količina svjetlosti')
    min_svjetlost = FloatField('Minimalna količina svjetlosti')
    max_ph = IntegerField('Maximalni pH')
    min_ph = IntegerField('Minimalni pH')
    max_vlaznost = IntegerField('Maximalni pH')
    min_vlaznost = IntegerField('Minimalni pH')
    max_temp = FloatField('Maximalna količina svjetlosti')
    min_temp = FloatField('Minimalna količina svjetlosti')

    submit = SubmitField('Dodaj novu biljku')


class Vaze (db.Model):
    __tablename__ = 'Posude'
    id = db.Column(db.Integer(), primary_key = True )
    ime_vaze = db.Column(db.String(50), unique = True, nullable = False)
    id_biljke = db.Column (db.Integer, db.ForeignKey('biljke.id'))




class Form_za_vazu (FlaskForm):
    ime_vaze = StringField('Kako želite nazvati ovu posudu?')
    odabir_biljke = StringField('Koju biljku želite posaditi?')


    submit = SubmitField('Dodaj novu posudu')

class Biljka_u_vazu (FlaskForm):

#end region

#region rute

@app.route('/popis_biljki')
def popis_biljki():
    pass


@app.route('/popis_vaza')
def popis_vaza():
    pass


@app.route('/dodaj_biljku', methods = ['GET' , 'POST'])
def dodaj_biljku():

    form = Form_za_biljke ()
    if form.validate_on_submit():
        #kada/ako stisnemo submit na formu desi se ovo dolje:
        nova_biljka = Biljke(
        ime_biljke = form.ime_biljke.data,
        slika = form.slika.data,
        max_svjetlost = form.max_svjetlost.data,
        min_svjetlost = form.min_svjetlost.data,
        max_ph = form.max_ph.data,
        min_ph = form.min_ph.data,
        max_vlaznost = form.max_vlaznost.data,
        min_vlaznost = form.min_vlaznost.data,
        max_temp = form.max_temp.data,
        min_temp = form.min_temp.data
        )
    #napravila sam objekt biljku, pomocu klase koju sam izradila i uzimajuci podatke koje sam dobila iz form-a

    db.session.add(nova_biljka)
    db.session.commit()
    flash('Nova biljka je uspješno dodana')
    #Tu sam dodala napravljen objekt i predala ga databazi kako bi ga upisala u databazu, jedan objekt = row podataka
    #Uz to i napravim neki flash message da korisnik zna da je uspjesno odradjeno


@app.route('/dodaj_vazu')
def dodaj_vazu():
    form = Form_za_vazu()
    
    if form.validate_on_submit():
        ime_biljke = form.odabir_biljke.data
        if ime_biljke == None:
            odabir_biljke = None
        else:
            odabir_biljke = Biljke.query.filter_by(ime_biljke).first()

        nova_vaza = Vaze (
            ime_vaze=form.ime_vaze.data,
            id_biljke = odabir_biljke.id)

    db.session.add(nova_vaza)
    db.session.commit()
    flash('Dodali ste vazu')
    pass


@app.route('/popis_vaza/dodaj_biljku')
def dodaj_biljku_vazi():
    pass

#end region