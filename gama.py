
from bottle import *
from auth import *
import requests


import psycopg2, psycopg2.extensions, psycopg2.extras
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)


# PRIKLOP NA BAZO
conn = psycopg2.connect(database=db, host=host, user=user, password=password)
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 
# Odkomentiraj, če želiš sporočila o napakah
debug(True)  # za izpise pri razvoju

@get('/')
def index():
    return "To je zacetna stran!"

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
def dodaj_trasakcijo():
    valute = cur.execute("""SELECT osnovna_valuta FROM devizni_tecaj 
                        GROUP BY osnovna_valuta
                        ORDER BY osnovna_valuta""")
    print(valute)
    return template("transakcija.html", naslov = "transakcija")
#SELECT osnovna_valuta FROM devizni_tecaj GROUP BY osnovna_valuta ORDER BY osnovna_valuta


 #Če dopišemo reloader=True, se bo sam restartal vsakič, ko spremenimo datoteko
run(host='localhost', port=8080, reloader=True)

