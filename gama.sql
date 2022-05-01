DROP TABLE IF EXISTS devizni_tecaj;
DROP TABLE IF EXISTS tip_narocila;
DROP TABLE IF EXISTS denarnica;
DROP TABLE IF EXISTS borza;
DROP TABLE IF EXISTS trasakcija;
DROP TABLE IF EXISTS uporabnik;

CREATE TABLE uporabnik (
    id_uporabnika INTEGER PRIMARY KEY,
    ime TEXT NOT NULL,
    priimek TEXT NOT NULL,  
    spol TEXT NOT NULL,
    datum_rojstva DATE NOT NULL,
    drzava TEXT NOT NULL,
    email TEXT NOT NULL,
    geslo TEXT NOT NULL, 
    datum_registracije DATE NOT NULL DEFAULT now()
);

CREATE TABLE borza (
    id_borze TEXT PRIMARY KEY,
    ime TEXT NOT NULL,
    vrsta TEXT NOT NULL,
    lokacija TEXT not NULL,
    povezava TEXT NOT NULL
);

CREATE TABLE denarnica (
    id_denarnice INTEGER PRIMARY KEY,
    uporabnik_id INTEGER REFERENCES uporabnik(id_uporabnika),
    borza_id TEXT REFERENCES borza(id_borze)
);

CREATE TABLE trasakcija (
    id_transakcije INTEGER PRIMARY KEY,
    datum_cas TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT now(),
    iz_kolicine DOUBLE PRECISION,
    v_kolicino DOUBLE PRECISION,
    iz_valute TEXT,
    v_valuto TEXT
);

CREATE TABLE tip_narocila (
    transakcija_id INTEGER REFERENCES trasakcija(id_transakcije),
    vrsta_narocila TEXT,
    podvrsta_narocila TEXT NOT NULL
);

CREATE TABLE devizni_tecaj (
    osnovna_valuta TEXT,
    kotirajoca_valuta TEXT,
    valutno_razmerje DOUBLE PRECISION NOT NULL,
    datum_razmerja DATE NOT NULL
);
