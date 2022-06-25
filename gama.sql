DROP TABLE IF EXISTS devizni_tecaj;
DROP TABLE IF EXISTS transakcija;
DROP TABLE IF EXISTS borza;
DROP TABLE IF EXISTS uporabnik;

CREATE TABLE uporabnik (
    id_uporabnika INTEGER PRIMARY KEY SERIAL,
    ime TEXT NOT NULL,
    priimek TEXT NOT NULL,  
    spol TEXT NOT NULL,
    datum_rojstva DATE NOT NULL,
    drzava TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
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

CREATE TABLE transakcija (
    id_transakcije INTEGER PRIMARY KEY SERIAL,
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
    datum_razmerja DATE NOT NULL,
    PRIMARY KEY (osnovna_valuta, kotirajoca_valuta, datum_razmerja)
);


-- na začetku
GRANT ALL ON DATABASE sem2022_vitor TO rokr WITH GRANT OPTION;
GRANT ALL ON DATABASE sem2022_vitor TO matejr WITH GRANT OPTION;
GRANT ALL ON SCHEMA public TO rokr WITH GRANT OPTION;
GRANT ALL ON SCHEMA public TO matejr WITH GRANT OPTION;


-- po ustvarjanju tabel
GRANT ALL ON ALL TABLES IN SCHEMA public TO rokr WITH GRANT OPTION;
GRANT ALL ON ALL TABLES IN SCHEMA public TO matejr WITH GRANT OPTION;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO rokr WITH GRANT OPTION;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO matejr WITH GRANT OPTION;


GRANT CONNECT ON DATABASE sem2022_vitor TO javnost;
GRANT USAGE ON SCHEMA public TO javnost;

GRANT SELECT ON ALL TABLES IN SCHEMA public TO javnost;
GRANT INSERT ON uporabnik TO javnost;
GRANT INSERT ON transakcija TO javnost;
