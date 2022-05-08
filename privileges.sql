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

WITH t1 AS (
SELECT uporabnik_id,
       borza_id,
       id_denarnice, 
       valuta,
       COALESCE(sum(trx.v_kolicino), 0) AS buy
FROM denarnica AS wal
     INNER JOIN transakcija AS trx ON wal.id_denarnice = trx.denarnica_id
     INNER JOIN tip_narocila AS tip ON  trx.id_transakcije = tip.transakcija_id
WHERE wal.uporabnik_id = 1001 AND tip.podvrsta_narocila = 'BUY' AND tip.vrsta_narocila = 'T'
GROUP BY 1, 2, 3, 4 ),
t2 AS (
SELECT uporabnik_id,
       borza_id,
       id_denarnice, 
       valuta,
       COALESCE(sum(trx.iz_kolicine), 0) AS sell
FROM denarnica AS wal
     INNER JOIN transakcija AS trx ON wal.id_denarnice = trx.denarnica_id
     INNER JOIN tip_narocila AS tip ON  trx.id_transakcije = tip.transakcija_id
WHERE wal.uporabnik_id = 1001 AND tip.podvrsta_narocila = 'SELL' AND tip.vrsta_narocila = 'T'
GROUP BY 1, 2, 3, 4 )
SELECT t1.uporabnik_id,
       t1.borza_id,
       t1.id_denarnice, 
       t1.valuta,
       buy - sell AS amount
FROM t1 LEFT JOIN t2 ON t1.uporabnik_id = t2.uporabnik_id 