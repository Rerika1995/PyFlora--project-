
from flask import Flask, flash, redirect, session, render_template, url_for, jsonify
from flask_wtf import FlaskForm
import json
from sqlalchemy import true
from wtforms import StringField, SubmitField, FloatField, IntegerField, PasswordField
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from datetime import datetime 
from flask_migrate import Migrate
from flask_login import login_user, LoginManager, login_required,logout_user, current_user, UserMixin
from Repository.data_creator import sensor_data
from Repository.read_temp import get_temp
#from Repository.user import CreateUser

#User = CreateUser("Sara", "Jones", "sara.jones@gmail.com", "SaraJones", "MojaLozinka12345")

app = Flask(__name__, template_folder='template')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/biljke.sqlite'
app.config['SECRET_KEY'] = 'tajni_kljuc'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_TIMEOUT'] = 15

moment = Moment(app) #izradimo objek iz ove klase, objek koj ce nam omogucit azuriranje baze podataka, predamu mu app
db = SQLAlchemy(app)
migrate = Migrate(app,db)

#flask Login configuration 

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


#region Class

class User (db.Model, UserMixin):
    __tablename__ = 'User'
    id = db.Column(db.Integer(), primary_key = True )
    ime = db.Column(db.String(50), nullable = False)
    prezime = db.Column (db.String())
    email = db.Column (db.String(50), unique = True , nullable = False)
    username = db.Column(db.String(50), unique = True , nullable = False)
    password = db.Column (db.Integer(), nullable = False)


#NAPRAVI GA U TERMINALU KASNIJE

class Biljke (db.Model):
    __tablename__ = 'Biljke'
    id = db.Column(db.Integer(), primary_key = True )
    ime_biljke = db.Column(db.String(50), unique = True , nullable = False)
    slika = db.Column (db.String(), nullable = False, default = 'prazna_vaza.jpg')
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
    __tablename__ = 'Vaze'
    id = db.Column(db.Integer(), primary_key = True )
    ime_vaze = db.Column(db.String(50), unique = True, nullable = False)
    id_biljke = db.Column (db.Integer, db.ForeignKey('Biljke.id'))


class Form_za_vazu (FlaskForm):
    ime_vaze = StringField('Kako želite nazvati ovu vazu?')
    odabir_biljke = StringField('Koju biljku želite posaditi? Napišite točno kao u prikazano u popisu')


    submit = SubmitField('Dodaj novu vazu')


class Profil (FlaskForm):
    ime= StringField('Upišite novo ime')
    prezime = StringField('Upišite novo prezime')
    email = StringField('Upišite novi email')
    username = StringField('Odaberite novi username')
    password = PasswordField('Odaberite novi password')

    submit = SubmitField('Promjenite svoje podatke')


class Login_form (FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')

    submit = SubmitField('Promjenite svoje podatke')

class Biljka_u_vazu (FlaskForm):
    pass

db.create_all()



#end region




#region rute




@app.route('/', methods = ['GET'])
@login_required
def index():
    res = Vaze.query.all()
    print("[VAZE GET RES] ", res)
    vaza_id = None
    return render_template('index.html', Vaze = res , vaza_id=vaza_id)


@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = Login_form()
    user = User.query.get(1)

    if form.validate_on_submit():
        if user.username == form.username.data and user.password == form.password.data:
            print('correct')
            login_user(user)
            return redirect("/")

        else:
            print('wrong data')
            flash('Wrong data, try again')

    return render_template('login.html', form=form) 


@app.route('/logout', methods = ['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('You are logged out!')

    return redirect('/login')    




@app.route('/index_senzor', methods = ['GET', 'POST'])
def index_senzor():
    res = Vaze.query.all()
    biljke = Biljke.query.all()
    temp = 30
    vlaznost, ph, light= sensor_data() #kako sada napunim te varjable koje cu koristit?
    print(vlaznost)
    print(vlaznost, ph, light, temp)

    return render_template('index_senzor.html', vaze = res, biljke = biljke, vlaznost = vlaznost, ph = ph, light = light, temp = temp)

@app.route('/profil', methods = ['GET' , 'POST']) 
@login_required
def profil():
    user=User.query.get(1)

    #OVDJE GA PRVO ISPISI

    #DOLJE DAJ MOGUCNOST ZA MJENJANJE

    form = Profil ()
    if form.validate_on_submit():
        #kada/ako stisnemo submit na formu desi se ovo dolje:


        if form.ime.data == "":
            print('no changes')
        else:
            user.ime = form.ime.data

        if form.prezime.data == "":
            pass
        else:
            user.prezime = form.prezime.data


        if form.email.data == "":
            pass
        else:
            user.email = form.email.data

        if form.username.data == "":
            pass
        else:
            user.username = form.username.data

        if form.password.data == "":
            pass
        else:
            user.password = form.password.data

        print(f' Nakon if-a {user.ime}{user.prezime} {user.username}{user.password}')


        db.session.commit()
        flash('Vaši podaci su promjenjeni')

    return render_template('Profil.html', form = form , user = user)
        

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
    #render_template('dodaj_biljku.html', form=form, Biljke = Biljke)

    return render_template('dodaj_biljku.html', form=form, Biljke = Biljke)


@app.route('/dodaj_vazu', methods = ['GET', 'POST'])
def dodaj_vazu():
    form = Form_za_vazu()
    biljke = Biljke.query.all()

    
    if form.validate_on_submit():

        odabir_biljke = Biljke.query.filter_by(ime_biljke = form.odabir_biljke.data).first()

        if form.odabir_biljke.data == '':
            nova_vaza = Vaze (
                ime_vaze=form.ime_vaze.data,
                id_biljke = None)
        else:
            nova_vaza = Vaze (
                ime_vaze=form.ime_vaze.data,
                id_biljke = odabir_biljke.id)
            print('inside dodavanje biljke')
        db.session.add(nova_vaza)
        db.session.commit()
        
        flash('Dodali ste vazu')

        #KORISTI try and EXCEPT ako biljka nije u bazi
    
    return render_template('dodaj_vazu.html', form = form, Vaze = Vaze, Biljke = Biljke, biljke = biljke)

#ovo radi osim prikaza biljki koje korisnik moze odabrati , u najgorem slucaju samo stavi u obican query all 

@app.route('/popis_vaza', methods = ['GET', 'POST'])
def popis_vaza():
    res = Vaze.query.all()
    print("[Vaze GET RES] ", res)
    return render_template('index01.html',Vaze = Vaze)



@app.route('/popis_biljki',  methods = ['GET'])
def popis_biljki():
    res = Biljke.query.all()
    print("[BILJKE GET RES] ", res)
    biljka_id = None
    return render_template('popis.html',Biljke = res, biljka_id = biljka_id)

'''
@app.route('/popis_biljki_one',  methods = ['GET'])
def biljka_get():
    res = Biljke.query.get(1)
    print("[BILJKE GET RES] ", res.ime_biljke)
    return {'Status':'OK'}
'''


@app.route('/biljka_edit/<biljka_id>', methods = ['GET' , 'POST'])
def biljka_edit(biljka_id):
    print(biljka_id)
    biljka = Biljke.query.filter_by(id=biljka_id).first()
    print(biljka)
    print(biljka.id)

    form = Form_za_biljke()

    if form.validate_on_submit():
        print(form.ime_biljke.data)

        print('form is validated')
        
        if form.ime_biljke.data == "":
            print('no changes')
        else:
            biljka.ime_biljke = form.ime_biljke.data
            print(biljka.ime_biljke)

        if form.slika.data == "":
            print('no changes')
        else:
            biljka.slika = form.slika.data

        if form.max_svjetlost.data == "":
            print('no changes')
        else:
            biljka.max_svjetlost = form.max_svjetlost.data

        if form.max_svjetlost.data == "":
            print('no changes')
        else:
            biljka.max_svjetlost = form.max_svjetlost.data
                    
        if form.min_svjetlost.data == "":
            print('no changes')
        else:
            biljka.max_svjetlost = form.min_svjetlost.data
            
        if form.max_ph.data == "":
            print('no changes')
        else:
            biljka.max_ph = form.max_ph.data
            
        if form.min_ph.data == "":
            print('no changes')
        else:
            biljka.min_ph = form.min_ph.data
            
        if form.max_vlaznost == "":
            print('no changes')
        else:
            biljka.max_vlaznost = form.max_vlaznost.data
            
        if form.min_vlaznost.data == "":
            print('no changes')
        else:
            biljka.min_vlaznost = form.min_vlaznost.data
            
        if form.max_temp.data == "":
            print('no changes')
        else:
            biljka.max_temp = form.max_temp.data
            
        if form.min_temp.data == "":
            print('no changes')
        else:
            biljka.min_temp = form.min_temp.data

        #MOGU LI OVO IKAKO NAPISATI U FOR PETLJI, KAZE DA NIJE ITERABILE
        print(biljka.ime_biljke)
        db.session.commit()


    return render_template('biljka_edit.html', biljka = biljka, biljka_id=biljka_id , form = form)


@app.route ('/delete_biljka/<biljka_id>', methods = ['GET' , 'POST'])
def delete_biljka(biljka_id):
    print('you are in delete route')
    biljka = Biljke.query.get(biljka_id)
    db.session.delete(biljka) #PROVJERI DA LI JE OK
    db.session.commit()
    return redirect("/popis_biljki")


@app.route('/vaza_edit/<vaza_id>', methods = ['GET', 'POST'])
def vaza_edit(vaza_id):
    form = Form_za_vazu()
    vaza = Vaze.query.get(vaza_id)
    biljka = Biljke.query.all()
    vaza_id=vaza.id
    print(vaza_id)

    if form.validate_on_submit():
        print('form is validated')

        odabir_biljke = Biljke.query.filter_by(ime_biljke = form.odabir_biljke.data).first()
        
        if form.ime_vaze.data == "":
            print('no changes')
        else:
            vaza.ime_vaze = form.ime_vaze.data

        if form.odabir_biljke.data == "":
            print('no changes')
        else:
            vaza.id_biljke = odabir_biljke.id

        db.session.commit()



    return render_template('vaza_edit.html', vaza = vaza, form=form, biljka=biljka , vaza_id=vaza_id )







@app.route ('/delete_vaza/<vaza_id>', methods = ['GET' , 'POST'])
def delete_vaza(vaza_id):
    vaza = Vaze.query.get(vaza_id)
    db.session.delete(vaza) #PROVJERI DA LI JE OK
    db.session.commit()
    return redirect("/")


@app.route ('/delete_biljkaUVazi/<vaza_id>', methods = ['GET' , 'POST'])
def delete_biljkaUVazi(vaza_id):
    vaza=Vaze.query.get(vaza_id)
    vaza.id_biljke = None
    db.session.commit()
    return redirect("/")


@app.route ('/vaza_edit_senzor/<vaza_id>', methods = ['GET' , 'POST'])
def vaza_edit_senzor(vaza_id):
    vaza=Vaze.query.get(vaza_id)
    temp = 25
    vlaznost, ph, light= sensor_data() #kako sada napunim te varjable koje cu koristit?


    return render_template ('vaza_edit_senzor.html', vaza = vaza, temp = temp , vlaznost = vlaznost , ph=ph , light = light, vaza_id = vaza_id)



    #napravila sam objekt biljku, pomocu klase koju sam izradila i uzimajuci podatke koje sam dobila iz form-a




     




if __name__ == '__main__':
    app.run(debug=True)