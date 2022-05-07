import imp
from traceback import print_tb

from auth import *
import csv

import psycopg2, psycopg2.extensions, psycopg2.extras
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE) # se znebimo problemov s šumniki



conn = psycopg2.connect(database=db, host=host, user=user, password=password)
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 


def ustvari_tabele():
    with open('gama.sql') as f:
        koda = f.read()
    cur.execute(koda)
    conn.commit()
    print("Uspesno ustvaril tabele!")

ustvari_tabele()

def pobrisi_tabelo(tabela):
    cur.execute("""
        DROP TABLE {0};
    """.format(tabela))
    conn.commit()
    print("Uspesno pobrisal tabelo!")

#pobrisi_tabelo("tip_narocila")


def uvoziCSV(tabela):
    with open('podatki/{0}'.format(tabela)) as csvfile:
        podatki = csv.reader(csvfile)
        next(podatki)
        for r in podatki:
            r = [None if x in ('', '-') else x for x in r]
            if "borza.csv" in tabela:
                cur.execute("""
                    INSERT INTO borza
                    (id_borze, ime, vrsta, lokacija, povezava)
                    VALUES (%s, %s, %s, %s, %s)
                """, r)
            elif "crypto.csv" in tabela:
                cur.execute("""
                    INSERT INTO devizni_tecaj
                    (osnovna_valuta, kotirajoca_valuta, valutno_razmerje, datum_razmerja)
                    VALUES (%s, %s, %s, %s)
                """, r)
        conn.commit()
        print("Uspesno uvozil csv datoteko!")

uvoziCSV("borze/borza.csv")
uvoziCSV("crypto/crypto.csv")


def uvozSQL(tabela):
    with open('podatki/{0}'.format(tabela)) as sqlfile:
        koda = sqlfile.read()
        cur.execute(koda)
    conn.commit()
    print("Uspesno nalozil podatke!")

uvozSQL("uporabniki/uporabnik.sql")