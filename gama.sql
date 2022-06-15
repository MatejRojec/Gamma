DROP TABLE IF EXISTS devizni_tecaj;
DROP TABLE IF EXISTS transakcija;
DROP TABLE IF EXISTS borza;
DROP TABLE IF EXISTS uporabnik;
DROP SEQUENCE IF EXISTS "ustevec";
DROP SEQUENCE IF EXISTS "tstevec";

CREATE SEQUENCE "ustevec" START 1;

CREATE TABLE uporabnik (
    id_uporabnika INTEGER DEFAULT NEXTVAL('ustevec') PRIMARY KEY,
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
    id_borze INTEGER PRIMARY KEY,
    ime TEXT NOT NULL,
    vrsta TEXT NOT NULL,
    lokacija TEXT,
    povezava TEXT NOT NULL
);


CREATE SEQUENCE "tstevec" START 1;

CREATE TABLE transakcija (
    id_transakcije INTEGER DEFAULT NEXTVAL('tstevec') PRIMARY KEY,
    uporabnik_id INTEGER REFERENCES uporabnik(id_uporabnika),
    borza_id INTEGER REFERENCES borza(id_borze),
    datum_cas TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT now(),
    iz_kolicine DOUBLE PRECISION,
    v_kolicino DOUBLE PRECISION,
    iz_valute TEXT,
    v_valuto TEXT,
    tip_narocila TEXT NOT NULL
);


CREATE TABLE devizni_tecaj (
    osnovna_valuta TEXT,
    kotirajoca_valuta TEXT,
    valutno_razmerje DOUBLE PRECISION NOT NULL,
    datum_razmerja DATE NOT NULL
);