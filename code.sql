-- na začetku
GRANT ALL ON DATABASE sem2022_vitor TO rokr WITH GRANT OPTION;
GRANT ALL ON DATABASE sem2022_vitor TO matejr WITH GRANT OPTION;
GRANT ALL ON SCHEMA public TO rokr WITH GRANT OPTION;
GRANT ALL ON SCHEMA public TO matejr WITH GRANT OPTION;

--GRANT CONNECT ON DATABASE sem2022_vitor TO javnost;
--GRANT USAGE ON SCHEMA public TO javnost;

-- po ustvarjanju tabel
GRANT ALL ON ALL TABLES IN SCHEMA public TO rokr WITH GRANT OPTION;
GRANT ALL ON ALL TABLES IN SCHEMA public TO matejr WITH GRANT OPTION;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO rokr WITH GRANT OPTION;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO matejr WITH GRANT OPTION;
--GRANT SELECT ON ALL TABLES IN SCHEMA public TO javnost;

-- dodatne pravice za uporabo aplikacije
--GRANT INSERT ON tabela TO javnost;
--GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO javnost;



-- za prikas borz in stanj na denarnicah
WITH t1 AS (SELECT uporabnik_id,
                    borza_id,
                    iz_valute AS valuta,
                    sum(iz_kolicine) AS x
FROM transakcija AS trx
WHERE uporabnik_id = 1001
GROUP BY 1, 2, 3),
t2 AS (SELECT uporabnik_id,
               borza_id,
               v_valuto AS valuta,
               sum(v_kolicino) AS y
FROM transakcija AS trx
WHERE uporabnik_id = 1001 
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
