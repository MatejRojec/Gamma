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
        vsiPodatki = [vrstica for vrstica in podatki]
        glava = vsiPodatki[0]
        vrstice = vsiPodatki[1:]
        ime_tabele = tabela.split("/")[-1].replace(".csv", "")
        stolpci = ", ".join(glava)
        zacetek = "INSERT INTO " + ime_tabele + " (" + stolpci + ") "
        for r in vrstice:
            neki = "('" +"', '".join(r) + "')"
            izvedi = zacetek + " VALUES " + neki + " RETURNING id_borze "
            cur.execute(izvedi)
            rid, = cur.fetchone()
            print("Uvožena občina %s z ID-jem %s" % (r[0], rid))
        conn.commit()
uvoziCSV("borze/borza.csv")


def uvozSQL(tabela):
    with open('podatki/{0}'.format(tabela)) as sqlfile:
        koda = sqlfile.read()
        cur.execute(koda)
    conn.commit()
    print("Uspesno nalozil podatke!")

uvozSQL("uporabniki/uporabnik.sql")