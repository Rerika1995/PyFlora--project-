from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from datetime import datetime 

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/biljke.sqlite'

moment = Moment(app) #izradimo objek iz ove klase, objek koj ce nam omogucit azuriranje baze podataka
db = SQLAlchemy(app)

#Region Class

class Biljke ():
    __tablename__ = 'biljke'
    id = db.Column(db.Integer)



#endregion