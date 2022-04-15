import imp
from traceback import print_tb

import psycopg2 # potrebna knjiznica za dostop do postgrSQL
import csv
# dostop do baze
from auth import *



baza_datoteka = db

conn_string = 'host={0} user={1} password={2}'.format(host, user, password)

#with psycopg2.connect(conn_string) as baza:
#    with open('gama.sql') as f:
#        koda = f.read()
#    cur = baza.cursor()
#    cur.executescript(koda)

def uvoziCSV(cur, tabela):
    with open('podatki/{0}'.format(tabela)) as csvfile:
        podatki = csv.reader(csvfile)
        vsiPodatki = [vrstica for vrstica in podatki]
        glava = vsiPodatki[0]
        vrstice = vsiPodatki[1:]
        #nam izvede vec SQL stavkov na enkrat
        cur.executemany(
            "INSERT INTO {0} ({1}) VALUES ({2})".format(
                tabela, ",".join(glava), ",".join(['?']*len(glava)), vrstice) # morda treba '?' zamenjati
            )


