
from flask import Flask, flash, session, render_template, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, IntegerField
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from datetime import datetime 
from flask_migrate import Migrate
#from Repository.user import CreateUser

#User = CreateUser("Sara", "Jones", "sara.jones@gmail.com", "SaraJones", "MojaLozinka12345")

app = Flask(__name__, template_folder='template')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/biljke.sqlite'
app.config['SECRET_KEY'] = 'tajni_kljuc'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

moment = Moment(app) #izradimo objek iz ove klase, objek koj ce nam omogucit azuriranje baze podataka, predamu mu app
db = SQLAlchemy(app)
migrate = Migrate(app,db)


#region Class

class User (db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer(), primary_key = True )
    ime = db.Column(db.String(50), nullable = False)
    prezime = db.Column (db.String())
    email = db.Column (db.String(50), unique = True , nullable = False)
    username = db.Column(db.String(50), unique = True , nullable = False)
    password = db.Column (db.Integer(), nullable = False)

#User(ime='Erika', prezime = 'Rerecic', email = 'erika.rerecic@gmail.com', username = 'Rerika', password ='lozinka1234')
#NAPRAVI GA U TERMINALU KASNIJE

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

#Kada budemo zvali podatke biljke iz baze Vaza koristimo definiran backref kako bi dosli do njih

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
    id_biljke = db.Column (db.Integer, db.ForeignKey('Biljke.id'))


class Form_za_vazu (FlaskForm):
    ime_vaze = StringField('Kako želite nazvati ovu posudu?')
    odabir_biljke = StringField('Koju biljku želite posaditi? Napišite točno kao u prikazano u popisu')


    submit = SubmitField('Dodaj novu posudu')


class Profil (FlaskForm):
    ime= StringField('Kako želite nazvati ovu posudu?')
    prezime = StringField('Koju biljku želite posaditi?')
    email = StringField('Koju biljku želite posaditi?')
    username = StringField('Koju biljku želite posaditi?')
    password = StringField('Koju biljku želite posaditi?')


    submit = SubmitField('Dodaj novu posudu')


class Biljka_u_vazu (FlaskForm):
    pass




#end region

#region rute


@app.route('/')
def index():
  return render_template('index.html')

@app.route('/profil', methods = ['GET' , 'POST'])  #da li ovo moze ovako i ako da, moram li koristiti methods tu?
def profil():
    user=User[1]

    #OVDJE GA PRVO ISPISI

    #DOLJE DAJ MOGUCNOST ZA MJENJANJE

    form = Profil ()
    if form.validate_on_submit():
        #kada/ako stisnemo submit na formu desi se ovo dolje:
        ime = form.ime.data,
        prezime = form.prezime.data,
        email = form.email.data,
        username = form.username.data,
        password = form.password.data

        if ime != '':
            pass
        else:
            user.ime = ime

        if prezime != '':
            pass
        else:
            user.prezime = prezime

        if email != '':
            pass
        else:
            user.email = email

        if username != '':
            pass
        else:
            user.username = username

        if password != '':
            pass
        else:
            user.password = password

        db.session.commit()
        flash('Vaši podaci su promjenjeni')

    return render_template('template/Profil.html', form = form , user = user)
        

#PROBLEM- ovo ce promjenit cjelog usera a ne samo djelove 


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

    return render_template('dodaj_biljku.html', form=form, Biljke = Biljke)


@app.route('/dodaj_vazu', methods = ['GET', 'POST'])
def dodaj_vazu():
    form = Form_za_vazu()
    
    if form.validate_on_submit():
        ime_vaze = form.ime_vaze.data
        ime_biljke = form.odabir_biljke.data
        if ime_biljke == None:
            odabir_biljke = None
        elif ime_biljke not in Biljke: #da li se to tako poziva, baza? 
            odabir_biljke = None
        else:
            odabir_biljke = Biljke.query.filter_by(ime_biljke).first()

        nova_vaza = Vaze (
            ime_vaze=form.ime_vaze.data,
            id_biljke = odabir_biljke.id)

        db.session.add(nova_vaza)
        db.session.commit()
        flash('Dodali ste vazu')
    
    return render_template('dodaj_vazu.html')



@app.route('/popis_vaza/dodaj_biljku')
def dodaj_biljku_vazi():
    pass
    


#end region

    for biljka in Vaze.biljka: 
        if biljka.max_svjetlost < light:  #provjeri da li se tako proziva
            flash('Premjestite biljku na manje osvjetljeno mjesto')
        elif biljka.max_svjetlost > light:
            print ('')

        elif biljka.min_svjetlost < light:  #provjeri da li se tako proziva
            flash('Premjestite biljku na manje osvjetljeno mjesto')
        elif biljka.min_svjetlost > light:
            print ('')
        else:
            pass
        
        if biljka.ph < light:  #provjeri da li se tako proziva
            print('Premjestite biljku na manje osvjetljeno mjesto')
        elif biljka.ph > light:
            print ('')
        else:
            pass

        if biljka.max_vlaznost < vlaznost:  #provjeri da li se tako proziva
            print('Premjestite biljku na manje osvjetljeno mjesto')
        elif biljka.max_vlaznost > vlaznost:
            print ('')
        else:
            pass

        if biljka.min_vlaznost < vlaznost:  #provjeri da li se tako proziva
            print('Premjestite biljku na manje osvjetljeno mjesto') #kako prikazem??
        elif biljka.min_vlaznost > vlaznost:
            print ('')
        else:
            pass
    return render_template('dodaj_biljku.html')

    
     


def Senzor_read(vlaznost, ph, light, temp, Biljke, Vaze):
    pass



if __name__ == '__main__':
    app.run(debug=True)