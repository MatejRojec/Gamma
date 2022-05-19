
from bottle import *
from auth import *
import hashlib
from bottleext import *


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
    napaka = nastaviSporocilo()
    return template('registracija.html', naslov="Registracija", napaka=napaka)

@post('/registracija')
def registracija_post():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    ime = request.forms.get('ime')
    priimek = request.forms.get('priimek')
    spol = request.forms.get('spol')
    datum_rojstva = request.forms.get('datum_rojstva')
    drzava = request.forms.get('drzava')
    email = request.forms.get('email')
    geslo = request.forms.get('geslo')
    geslo2 = request.forms.get('geslo2')
 
    try: 
        cur.execute("SELECT * FROM uporabnik WHERE email = %s", [email])
        data = cur.fetchall()   
        if data != []:
            email = None
        else:
            email = email
    except:
        email = email
    if email is None:
        nastaviSporocilo('Registracija ni možna ta email je že v uporabi') 
        redirect('/registracija')
        return
    if len(geslo) < 4:
        nastaviSporocilo('Geslo mora imeti vsaj 4 znake.') 
        redirect(url('registracija_get'))
        return
    if geslo != geslo2:
        nastaviSporocilo('Gesli se ne ujemata.') 
        redirect(url('registracija_get'))
        return

    cur.execute("SELECT max(id_uporabnika) FROM uporabnik")
    id_uporabnika = cur.fetchall()

    id_uporabnika = id_uporabnika[0][0] + 1
    zgostitev = hashGesla(geslo)
    print([id_uporabnika, ime, priimek, spol, datum_rojstva, drzava, email, zgostitev])
    try:
        cur.execute("""INSERT INTO 
        uporabnik (id_uporabnika, ime, priimek, spol, datum_rojstva, drzava, email, geslo) 
        VALUES  (%s, %s, %s, %s, %s, %s, %s, %s) """,
        [id_uporabnika, ime, priimek, spol, datum_rojstva, drzava, email, zgostitev])
    except:
        nastaviSporocilo('Registracija ni možna napačen vnos') 
        redirect(url('registracija_get'))
    #cur.execute("UPDATE oseba SET username = ?, password = ? WHERE emso = ?", (username, zgostitev, emso))
    #response.set_cookie('username', username, secret=skrivnost)
    
    redirect(url('uporabnik_get', id_uporabnika=id_uporabnika))

@get('/prijava') # lahko tudi @route('/prijava')
def prijava_get():
    return template("prijava.html", naslov = "Prijava")

@post('/prijava') # or @route('/prijava', method='POST')
def prijava_post():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    email = request.forms.get('email')
    geslo = request.forms.get('geslo')
    hashBaza = None
    try: 
        cur.execute("SELECT geslo FROM uporabnik WHERE email = %s", [email])
        hashBaza = cur.fetchall()[0][0]
    except:
        hashBaza = None
    if hashBaza is None:
        nastaviSporocilo('Elektronski naslov ali geslo nista ustrezni') 
        redirect(url('prijava_get'))
        return
    if hashGesla(geslo) != hashBaza:
        nastaviSporocilo('Elektronski naslov ali geslo nista ustrezni') 
        redirect(url('prijava_get'))
        return    
    cur.execute('SELECT id_uporabnika FROM uporabnik WHERE email = %s', [email])
    id_uporabnika = cur.fetchall()[0][0]
    redirect(url('uporabnik_get', id_uporabnika=id_uporabnika))






@get('/uporabnik/<id_uporabnika>')
def uporabnik_get(id_uporabnika):
    id_uporabnika = int(id_uporabnika)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('''
    WITH t1 AS (SELECT uporabnik_id,
                    borza_id,
                    iz_valute AS valuta,
                    sum(iz_kolicine) AS x
    FROM transakcija AS trx
    WHERE uporabnik_id = %s
    GROUP BY 1, 2, 3),
    t2 AS (SELECT uporabnik_id,
                borza_id,
                v_valuto AS valuta,
                sum(v_kolicino) AS y
    FROM transakcija AS trx
    WHERE uporabnik_id = %s 
    GROUP BY 1, 2, 3),
    t3 AS (SELECT t1.uporabnik_id,
                b.ime,
                t1.valuta, 
                COALESCE(y, 0) - COALESCE(x, 0) AS amount       
    FROM t1 
        FULL JOIN t2 ON t1.uporabnik_id = t2.uporabnik_id 
            AND t1.valuta = t2.valuta 
            AND t1.borza_id = t2.borza_id
        LEFT JOIN borza AS b ON b.id_borze = t1.borza_id
    WHERE t1.valuta <> ''),
    t4 AS (SELECT t2.uporabnik_id,
                b.ime,
                t2.valuta, 
                COALESCE(y, 0) - COALESCE(x, 0) AS amount       
    FROM t2 
        FULL JOIN t1 ON t1.uporabnik_id = t2.uporabnik_id 
            AND t1.valuta = t2.valuta 
            AND t1.borza_id = t2.borza_id
        LEFT JOIN borza AS b ON b.id_borze = t2.borza_id
    WHERE t2.valuta <> '')
    SELECT * FROM t3 
    UNION 
    SELECT * FROM t4
    ''', [id_uporabnika]*2)
    data = cur.fetchall()
    cur.execute('''
    WITH t1 AS (SELECT DISTINCT id_borze FROM borza),
    excluded AS (SELECT DISTINCT borza_id FROM transakcija WHERE uporabnik_id = %s)
    SELECT t1.id_borze, t3.ime FROM t1 LEFT JOIN excluded AS t2 ON t2.borza_id = t1.id_borze 
    LEFT JOIN borza AS t3 ON t3.id_borze = t1.id_borze 
    WHERE t2.borza_id IS NULL
    ORDER BY 2
    ''', [id_uporabnika])
    uporabnik_borze = cur.fetchall()
    cur.execute("SELECT osnovna_valuta FROM devizni_tecaj GROUP BY osnovna_valuta")
    valute = cur.fetchall()
    aum = 100  
    #data = [] #to bojo podatki o uporabniku: borz denarnice in stanje
    #data = [['BitStamp', 'DenarnicaBTC', 34],['BitStamp', 'DenarnicaETH', 12],['BitStamp', 'DenarnicaUSD', 23400],['Binance', 'DenarnicaBTC', 1],['Binance', 'DenarnicaADA', 12000], ['Coinbase', 'DenarnicaUSD', 100]]
    
    return template('uporabnik.html',aum = aum, data = data , id_uporabnika = id_uporabnika, uporabnik_borze = uporabnik_borze, valute=valute)


@post('/uporabnik/<id_uporabnika>')
def uporabnik_post(id_uporabnika):
    id_uporabnika = int(id_uporabnika)
    denarnica = request.forms.get('valuta')
    ime_borze = request.forms.get('ime_borze')
    borza_id = request.forms.get("id_borze")
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(" SELECT MAX(id_transakcije) FROM transakcija")
    id_transakcije = 1 + cur.fetchall()[0][0]
    if ime_borze == None:
        cur.execute(''' 
        INSERT INTO transakcija (id_transakcije, uporabnik_id, borza_id, iz_kolicine, v_kolicino, v_valuto, tip_narocila) 
        VALUES (%s,%s,%s,%s,%s,%s,%s);
        ''',
        [id_transakcije, id_uporabnika, borza_id, 0, 0, "USD", "A"])
        redirect(url('uporabnik_get', id_uporabnika=id_uporabnika))
    else:
        cur.execute("SELECT id_borze FROM borza WHERE ime = %s ", [ime_borze])
        borza_id = cur.fetchall()[0][0]
        cur.execute(''' 
        SELECT v_valuto FROM transakcija 
        WHERE uporabnik_id = %s AND borza_id = %s AND v_valuto <> ''
        GROUP BY v_valuto
        ''', [id_uporabnika, borza_id])
        uporabnik_valute = cur.fetchall()
        if [denarnica] in uporabnik_valute:
            nastaviSporocilo("Ta denarnica že obstaja")
            redirect(url('uporabnik_get', id_uporabnika=id_uporabnika))
        else:
            print(id_transakcije, id_uporabnika, borza_id, 0, 0, denarnica, "A")
            cur.execute(''' 
            INSERT INTO transakcija (id_transakcije, uporabnik_id, borza_id, iz_kolicine, v_kolicino, v_valuto, tip_narocila) 
            VALUES (%s,%s,%s,%s,%s,%s,%s);
            ''',
            [id_transakcije, id_uporabnika, borza_id, 0, 0, denarnica, "A"])
            redirect(url('uporabnik_get', id_uporabnika=id_uporabnika))
        


@get('/transakcija/<id_uporabnika>')
def trasakcija_get(id_uporabnika):
    #tu bomo naredili transakcijo
    return "blalalal"
    #cur.execute("SELECT osnovna_valuta FROM devizni_tecaj GROUP BY osnovna_valuta ORDER BY osnovna_valuta")
    #valute = sum(cur.fetchall(), [])
    #cur.execute("SELECT * FROM transakcija")
    #trans = cur.fetchall()
    #return template("testiranje.html", naslov = "transakcija", valute = valute, trans=trans)
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

