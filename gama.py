
from bottle import *
from auth import *
import requests
import hashlib


import psycopg2, psycopg2.extensions, psycopg2.extras
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)


# PRIKLOP NA BAZO
conn = psycopg2.connect(database=db, host=host, user=user, password=password)
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 
# Odkomentiraj, če želiš sporočila o napakah
debug(True)  # za izpise pri razvoju


skrivnost = 'laqwXUtKfHTp1SSpnkSg7VbsJtCgYS89QnvE7PedkXqbE8pPj7VeRUwqdXu1Fr1kEkMzZQAaBR93PoGWks11alfe8y3CPSKh3mEQ'

napakaSporocilo = None
def nastaviSporocilo(sporocilo=None):
    global napakaSporocilo
    staro = napakaSporocilo
    napakaSporocilo = sporocilo
    return staro

#funkcija za piškotke
def id_uporabnik():
    if request.get_cookie("id", secret = skrivnost):
        piskotek = request.get_cookie("id", secret = skrivnost)
        return piskotek
    else:
        return 0



@get('/')
def index():
    return "To je zacetna stran!"
    
def hashGesla(s):
    m = hashlib.sha256()
    m.update(s.encode("utf-8"))
    return m.hexdigest()

@get('/registracija')
def registracija_get():
    return template('registracija.html')

@post('/registracija')
def registracija_post():
    emso = request.forms.emso
    username = request.forms.username
    password = request.forms.password
    password2 = request.forms.password2
    if emso is None or username is None or password is None or password2 is None:
        nastaviSporocilo('Registracija ni možna') 
        redirect('/registracija')
    try: 
        uporabnik = cur.execute("SELECT * FROM oseba WHERE emso = ?", (emso, )).fetchone()
    except:
        uporabnik = None
    if uporabnik is None:
        nastaviSporocilo('Registracija ni možna') 
        redirect('/registracija')
        return
    if len(password) < 4:
        nastaviSporocilo('Geslo mora imeti vsaj 4 znake.') 
        redirect('/registracija')
        return
    if password != password2:
        nastaviSporocilo('Gesli se ne ujemata.') 
        redirect('/registracija')
        return
    zgostitev = hashGesla(password)
    cur.execute("UPDATE oseba SET username = ?, password = ? WHERE emso = ?", (username, zgostitev, emso))
    response.set_cookie('username', username, secret=skrivnost)
    redirect('/komitenti')

@get('/prijava') # lahko tudi @route('/prijava')
def prijavno_okno():
    return template("prijava.html", naslov = "Prijava")

@post('/prijava') # or @route('/prijava', method='POST')
def prijava():
    mail = request.forms.get('mail')
    geslo = request.forms.get('geslo')
    if preveri(mail, geslo):
        return "<p>Dobrodošel {0}.</p>".format(mail)
    else:
        return '''<p>Napačni podatki za prijavo.
Poskusite <a href="/prijava">še enkrat</a></p>'''

def preveri(mail, geslo):
    return mail=="admin" and geslo=="admin"


@get('/stanje')
def prever_stanje():
    return template("stanje.html")

@get('/transakcija')
def trasakcija():
    cur.execute("SELECT osnovna_valuta FROM devizni_tecaj GROUP BY osnovna_valuta ORDER BY osnovna_valuta")
    valute = sum(cur.fetchall(), [])
    cur.execute("SELECT * FROM transakcija")
    trans = cur.fetchall()
    return template("testiranje.html", naslov = "transakcija", valute = valute, trans=trans)
 #Če dopišemo reloader=True, se bo sam restartal vsakič, ko spremenimo datoteko


@post('/transakcija')
def dodaj_transakcijo():
    crypto = str(request.forms.get('crypto'))
    iz_kolicine = int(request.forms.get('iz_kolicine'))
    v_kolicino = int(request.forms.get('v_kolicino'))

    cur.execute("""SELECT id_transakcije FROM transakcija
                    ORDER BY id_transakcije""")
    kljuci = sum(cur.fetchall(), [])
    if len(kljuci) == 0:
        id_transakcije = 1
    else:
        id_transakcije = kljuci.pop() + 1
    cur.execute("""
    INSERT INTO transakcija (id_transakcije, iz_kolicine, v_kolicino, iz_valute, v_valuto)
    VALUES (%s, %s, %s, %s, %s)"""
    , [id_transakcije, iz_kolicine, v_kolicino, 'USD', crypto])
    redirect('/test')

@get('/denarnica')
def denarnica():
    pass




run(host='localhost', port=8080, reloader=True)

