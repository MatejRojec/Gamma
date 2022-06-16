
from bottle import *
from auth import *
import hashlib
from bottleext import *
from datetime import date




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


def hashGesla(s):
    m = hashlib.sha256()
    m.update(s.encode("utf-8"))
    return m.hexdigest()

def povezi():
    global conn
    conn = psycopg2.connect(database=db, host=host, user=user, password=password)


@get('/')
def index():
    znacka = id_uporabnik()
    print(znacka)
    return template('zacetna_stran.html', nalosv="Zacetna stran", znacka=znacka)
    
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
        redirect(url('registracija_get'))
        return
    if len(geslo) < 4:
        nastaviSporocilo('Geslo mora imeti vsaj 4 znake.') 
        redirect(url('registracija_get'))
        return
    if geslo != geslo2:
        nastaviSporocilo('Gesli se ne ujemata.') 
        redirect(url('registracija_get'))
        return


    
    zgostitev = hashGesla(geslo)
    print([ime, priimek, spol, datum_rojstva, drzava, email, zgostitev])
    try:
        cur.execute("""INSERT INTO 
        uporabnik (ime, priimek, spol, datum_rojstva, drzava, email, geslo) 
        VALUES  (%s, %s, %s, %s, %s, %s, %s) """,
        [ ime, priimek, spol, datum_rojstva, drzava, email, zgostitev])
        conn.commit()
    except:
        nastaviSporocilo('Registracija ni možna napačen vnos') 
        redirect(url('registracija_get'))
    #response.set_cookie('username', username, secret=skrivnost)
    cur.execute("SELECT id_uporabnika FROM uporabnik WHERE email == %s", [email])
    id_uporabnika = cur.fetchone()[0]
    
    redirect(url('uporabnik_get', id_uporabnika=id_uporabnika))

@get('/prijava') # lahko tudi @route('/prijava')
def prijava_get():
    napaka = nastaviSporocilo()
    return template("prijava.html", naslov = "Prijava", napaka=napaka)

@post('/prijava') # or @route('/prijava', method='POST')
def prijava_post():
    povezi()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    email = request.forms.get('email')
    geslo = request.forms.get('geslo')
    hashBaza = None
    try: 
        cur.execute("SELECT geslo FROM uporabnik WHERE email = %s", [email])
        hashBaza = cur.fetchone()[0]
    except:
        hashBaza = None
    if hashBaza is None:
        napaka = nastaviSporocilo('Elektronski naslov ali geslo nista ustrezni') 
        redirect(url('prijava_get'))
        return
    if hashGesla(geslo) != hashBaza:
        napaka = nastaviSporocilo('Elektronski naslov ali geslo nista ustrezni') 
        redirect(url('prijava_get'))
        return    
    cur.execute('SELECT id_uporabnika FROM uporabnik WHERE email = %s', [email])
    id_uporabnika = cur.fetchone()[0]
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
    aum = ''  
    #data = [] #to bojo podatki o uporabniku: borz denarnice in stanje
    #data = [['BitStamp', 'DenarnicaBTC', 34],['BitStamp', 'DenarnicaETH', 12],['BitStamp', 'DenarnicaUSD', 23400],['Binance', 'DenarnicaBTC', 1],['Binance', 'DenarnicaADA', 12000], ['Coinbase', 'DenarnicaUSD', 100]]
    napaka = nastaviSporocilo()
    return template('uporabnik.html',aum = aum, data = data , id_uporabnika = id_uporabnika, uporabnik_borze = uporabnik_borze, valute=valute, napaka=napaka)


@post('/uporabnik/<id_uporabnika>')
def uporabnik_post(id_uporabnika):
    id_uporabnika = int(id_uporabnika)
    denarnica = request.forms.get('valuta')
    ime_borze = request.forms.get('ime_borze')
    borza_id = request.forms.get("id_borze")
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if ime_borze == None:
        cur.execute(""" 
        INSERT INTO transakcija (uporabnik_id, borza_id, iz_kolicine, v_kolicino, v_valuto, tip_narocila) 
        VALUES (%s,%s,%s,%s,%s,%s);
        """,
        [id_uporabnika, borza_id, 0, 0, "USD", "A"])
        redirect(url('uporabnik_get', id_uporabnika=id_uporabnika))
    else:
        cur.execute("SELECT id_borze FROM borza WHERE ime = %s ", [ime_borze])
        borza_id = cur.fetchone()[0]
        cur.execute(""" 
        SELECT v_valuto FROM transakcija 
        WHERE uporabnik_id = %s AND borza_id = %s AND v_valuto <> ''
        GROUP BY v_valuto
        """, [id_uporabnika, borza_id])
        uporabnik_valute = cur.fetchall()
        if [denarnica] in uporabnik_valute:
            nastaviSporocilo("Ta denarnica že obstaja")
            redirect(url('uporabnik_get', id_uporabnika=id_uporabnika))
        else:
            print(id_uporabnika, borza_id, 0, 0, denarnica, "A")
            cur.execute(""" 
            INSERT INTO transakcija (uporabnik_id, borza_id, iz_kolicine, v_kolicino, v_valuto, tip_narocila) 
            VALUES (%s,%s,%s,%s,%s,%s);
            """,
            [id_uporabnika, borza_id, 0, 0, denarnica, "A"])
            #conn.commit()
            redirect(url('uporabnik_get', id_uporabnika=id_uporabnika))
            return


@get('/transakcija/<id_uporabnika>/<borza>')
def transakcija_get(id_uporabnika, borza):
    today = date.today()
    datum = today.strftime("%Y-%m-%d")
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT id_borze FROM borza WHERE ime = %s", [borza])
    borza_id = cur.fetchone()[0]

    cur.execute("""
    SELECT v_valuto FROM transakcija 
    WHERE uporabnik_id=%s AND borza_id = %s AND v_valuto <> ''
    GROUP BY v_valuto
    """, [int(id_uporabnika), int(borza_id)])
    valute = cur.fetchall()
    #valute = [['USD'], ['BTC'], ['ETH']]  
    napaka = nastaviSporocilo()
    return template("transakcija.html", 
    naslov ="Transakcija", borza=[borza_id, borza], datum=datum, valute=valute, id_uporabnika=id_uporabnika, napaka=napaka)


@post('/transakcija/<id_uporabnika>/<borza>')
def transkacija_post(id_uporabnika, borza):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    id_uporabnika = int(id_uporabnika)
    iz_valute = request.forms.get('iz_valute')
    v_valuto = request.forms.get('v_valuto')
    iz_kolicine = float(request.forms.get('kolicina'))
    datum_transakcije = request.forms.get('datum_transakcije')
    borza_id = int(request.forms.get('id_borze'))
    if iz_valute==v_valuto: #napaka
        nastaviSporocilo('Valuti morata biti različni, sicer transakcija ni možna!')
        redirect(url('transakcija_get', id_uporabnika=id_uporabnika, borza=borza))
        return
    elif iz_valute == 'USD': 
        cur.execute("""
        SELECT valutno_razmerje FROM devizni_tecaj
        WHERE osnovna_valuta = %s AND datum_razmerja = %s; 
        """, [v_valuto, datum_transakcije])
        razmerje = float(cur.fetchone()[0])
        v_kolicino = iz_kolicine / razmerje

        print([id_uporabnika, borza_id, datum_transakcije, iz_kolicine, v_kolicino, iz_valute, v_valuto, "T"])
        cur.execute(""" 
        INSERT INTO transakcija (uporabnik_id, borza_id, datum_cas, iz_kolicine, v_kolicino,iz_valute, v_valuto, tip_narocila) 
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s);
        """,
        [id_uporabnika, borza_id,datum_transakcije, iz_kolicine, v_kolicino, iz_valute, v_valuto, "T"])
        #conn.commit()
    elif v_valuto == 'USD': 
        cur.execute("""
        SELECT valutno_razmerje FROM devizni_tecaj
        WHERE osnovna_valuta = %s AND datum_razmerja = %s; 
        """, [iz_valute, datum_transakcije])
        razmerje = float(cur.fetchone()[0])
        v_kolicino = iz_kolicine * razmerje

        print([id_uporabnika, borza_id, datum_transakcije, iz_kolicine, v_kolicino, iz_valute, v_valuto, "T"])
        cur.execute(""" 
        INSERT INTO transakcija ( uporabnik_id, borza_id, datum_cas, iz_kolicine, v_kolicino,iz_valute, v_valuto, tip_narocila) 
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s);
        """,
        [id_uporabnika, borza_id, datum_transakcije, iz_kolicine, v_kolicino, iz_valute, v_valuto, "T"])
        #conn.commit()
    else:
        cur.execute("""
        SELECT valutno_razmerje FROM devizni_tecaj
        WHERE osnovna_valuta = %s AND datum_razmerja = %s; 
        """, [iz_valute, datum_transakcije])
        razmerje1 = float(cur.fetchone()[0])
        cur.execute("""
        SELECT valutno_razmerje FROM devizni_tecaj
        WHERE osnovna_valuta = %s AND datum_razmerja = %s; 
        """, [v_valuto, datum_transakcije])
        razmerje2 = float(cur.fetchone()[0])
        v_kolicino = iz_kolicine * (razmerje1/razmerje2)   

        print([id_uporabnika, borza_id,datum_transakcije, iz_kolicine, v_kolicino, iz_valute, v_valuto, "T"])
        cur.execute(""" 
        INSERT INTO transakcija (uporabnik_id, borza_id, datum_cas, iz_kolicine, v_kolicino,iz_valute, v_valuto, tip_narocila) 
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s);
        """,
        [id_uporabnika, borza_id, datum_transakcije, iz_kolicine, v_kolicino, iz_valute, v_valuto, "T"])
        #conn.commit()

    redirect(url('uporabnik_get', id_uporabnika=id_uporabnika))
    return 
    

@post('/depwith/<id_uporabnika>/<borza_id>')
def depwith_post(id_uporabnika, borza_id):
    id_uporabnika = int(id_uporabnika)
    valuta = request.forms.get('valuta')
    kolicina = float(request.forms.get('kolicina'))
    datum_narocila = request.forms.get('datum')
    narocilo = request.forms.get('narocilo')
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT ime FROM borza WHERE id_borze = %s", [borza_id])
    borza = cur.fetchone()[0]
    if narocilo == "D":
        print([id_uporabnika, int(borza_id), datum_narocila, 0, kolicina, valuta, narocilo])
        cur.execute(""" 
               INSERT INTO transakcija (uporabnik_id, borza_id, datum_cas, iz_kolicine, v_kolicino, v_valuto, tip_narocila) 
               VALUES (%s,%s,%s,%s,%s,%s,%s);
               """,
               [id_uporabnika, int(borza_id), datum_narocila, 0, kolicina, valuta, narocilo])
        #conn.commit()
        redirect(url('uporabnik_get', id_uporabnika=id_uporabnika))
    else:
        cur.execute('''
        WITH t0 AS (SELECT *
        FROM transakcija
        WHERE uporabnik_id = %s),

        t1 AS (SELECT uporabnik_id,
                            borza_id,
                            iz_valute AS valuta,
                            sum(iz_kolicine) AS x
        FROM t0 AS trx
        GROUP BY 1, 2, 3),

        t2 AS (SELECT uporabnik_id,
                    borza_id,
                    v_valuto AS valuta,
                    sum(v_kolicino) AS y
        FROM t0 AS trx 
        GROUP BY 1, 2, 3),

        t3 AS (SELECT t1.uporabnik_id,
                    b.id_borze,
                    t1.valuta, 
                    COALESCE(y, 0) - COALESCE(x, 0) AS amount       
        FROM t1 
            FULL JOIN t2 ON t1.uporabnik_id = t2.uporabnik_id 
                AND t1.valuta = t2.valuta 
                AND t1.borza_id = t2.borza_id
            LEFT JOIN borza AS b ON b.id_borze = t1.borza_id
        WHERE t1.valuta <> ''),

        t4 AS (SELECT t2.uporabnik_id,
                    b.id_borze,
                    t2.valuta, 
                    COALESCE(y, 0) - COALESCE(x, 0) AS amount       
        FROM t2 
            FULL JOIN t1 ON t1.uporabnik_id = t2.uporabnik_id 
                AND t1.valuta = t2.valuta 
                AND t1.borza_id = t2.borza_id
            LEFT JOIN borza AS b ON b.id_borze = t2.borza_id
        WHERE t2.valuta <> ''),

        t5 as(     
        SELECT * FROM t3 
        UNION 
        SELECT * FROM t4)

        SELECT t5.amount
        FROM t5 
        WHERE t5.id_borze = %s AND valuta = %s    
        ''',  [id_uporabnika, borza_id, valuta])
        stanje = cur.fetchone()[0]
        if stanje < kolicina:
            nastaviSporocilo('Stanje na denarnici je prenizko!')
            redirect(url('transakcija_get', id_uporabnika=id_uporabnika, borza=borza))
        else:
            print([10, id_uporabnika, int(borza_id), datum_narocila, kolicina, 0, valuta, narocilo])
            cur.execute(""" 
                   INSERT INTO transakcija (uporabnik_id, borza_id, datum_cas, iz_kolicine, v_kolicino, v_valuto, tip_narocila) 
                   VALUES (%s,%s,%s,%s,%s,%s,%s);
                   """,
                   [id_uporabnika, int(borza_id), datum_narocila, kolicina, 0, valuta, narocilo])
            #conn.commit()
            redirect(url('uporabnik_get', id_uporabnika=id_uporabnika))

    redirect(url('uporabnik_get', id_uporabnika=id_uporabnika))



@get('/about/')
def about():
    return template("about.html", naslov='O podjetju')


@get('/borze/')
def borze():
    conn = psycopg2.connect(database=db, host=host, user=user, password=password)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 
    cur.execute("SELECT ime, povezava FROM borza")
    data = cur.fetchall()
    return template("borze.html", naslov='Borze', data=data)

@get('/crypto/')
def crypto():
    sez = '1.5.2022,2.5.2022,3.5.2022,4.5.2022,5.5.2022,6.5.2022,7.5.2022,8.5.2022,9.5.2022,10.5.2022,11.5.2022,12.5.2022,13.5.2022,14.5.2022,15.5.2022,16.5.2022,17.5.2022,18.5.2022,19.5.2022,20.5.2022'
    return template("crypto.html", naslov='Crypto', sez=sez)


@get('/odjava/')
def odjava():
    #response.delete_cookie("id", path='/')
    redirect(url('index'))

run(host='localhost', port=8080, reloader=True)

