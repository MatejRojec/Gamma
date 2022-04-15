from genericpath import getsize
from bottle import *
import psycopg2

# KONFIGURACIJA
baza_datoteka = 'gama.db'

# Odkomentiraj, če želiš sporočila o napakah
debug(True)  # za izpise pri razvoju

@get('/')
def index():
    return """
    <html>
        <body>
            <p>
                To je zacezna stran
            </p>
            <form action="/prijava" method="get">
                <input value="Prijavi se" type="submit" />
            </form>
        </body>
    </html>
    """

@get('/prijava') # lahko tudi @route('/prijava')
def prijavno_okno():
    return """
    <html>
        <body>
            <form action="/prijava" method="post">
                <span class="neki">Uporabniško ime:</span> <input name="uime" type="text" />
                <span style="font-size:xx-large;text-decoration: underline">Geslo:</span> <input name="geslo" type="password" />
                <input value="Prijava" type="submit" />
            </form>
        </body>
    </html>
    """

# zahtevek POST
@post('/prijava') # or @route('/prijava', method='POST')
def prijava():
    uime = request.forms.get('uime')
    geslo = request.forms.get('geslo')
    if preveri(uime, geslo):
        return "<p>Dobrodošel {0}.</p>".format(uime)
    else:
        return '''<p>Napačni podatki za prijavo.
Poskusite <a href="/prijava">še enkrat</a></p>'''


def preveri(uime, geslo):
    return uime=="admin" and geslo=="admin"


# Če dopišemo reloader=True, se bo sam restartal vsakič, ko spremenimo datoteko
run(host='localhost', port=8080, reloader=True)