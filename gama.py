
from bottle import *
from auth import *


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

@get('/stanje')
def prever_stanje():
    return template("stanje.html")

@get('/transakcija')
def dodaj_trasakcijo():
    return template("transakcija.html")

# zahtevek POST
#@post('/prijava') # or @route('/prijava', method='POST')
#def prijava():
#    uime = request.forms.get('uime')
#    geslo = request.forms.get('geslo')
#    if preveri(uime, geslo):
#        return "<p>Dobrodošel {0}.</p>".format(uime)
#    else:
#        return '''<p>Napačni podatki za prijavo.
#Poskusite <a href="/prijava">še enkrat</a></p>'''

#def preveri(uime, geslo):
#    return uime=="admin" and geslo=="admin"


# Če dopišemo reloader=True, se bo sam restartal vsakič, ko spremenimo datoteko
run(host='localhost', port=8080, reloader=True)