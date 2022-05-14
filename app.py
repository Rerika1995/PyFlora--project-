from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, IntegerField
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from datetime import datetime 
from flask_migrate import Migrate

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/biljke.sqlite'

moment = Moment(app) #izradimo objek iz ove klase, objek koj ce nam omogucit azuriranje baze podataka, predamu mu app
db = SQLAlchemy(app)
migrate = Migrate(app,db)


#Region Class

class Biljke (db.Model):
    __tablename__ = 'Biljke'
    id = db.Column(db.Integer(), primary_key = True )
    ime_biljke = db.Column(db.String(50))
    slika = db.Column (db.String())
    max_svjetlost = db.Column (db.Float())
    min_svjetlost = db.Column (db.Float())
    max_ph = db.Column (db.Integer())
    min_ph = db.Column (db.Integer())
    max_vlaznost = db.Column (db.Integer())
    min_vlaznost = db.Column (db.Integer())
    max_temp = db.Column (db.Float())
    min_temp = db.Column (db.Float())


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


class User():
    
#endregion