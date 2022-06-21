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




-- dodatek z trenutnim tecajem v USD
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
WHERE t2.valuta <> ''),
t5 as(     
SELECT * FROM t3 
UNION 
SELECT * FROM t4)
SELECT t5.uporabnik_id,
       t5.ime,
       t5.valuta,
       t5.amount,
       t5.amount * COALESCE(valutno_razmerje, 1) as amount_usd
        FROM t5 
            left join devizni_tecaj dt
                on dt.osnovna_valuta = t5.valuta
                AND date(datum_razmerja) = date(now())


-- stanje denarnice na borzi 1 za denarnico ADA

WITH t0 AS (SELECT *
FROM transakcija
WHERE uporabnik_id = 1001),

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
WHERE t5.id_borze = 1 AND valuta = 'ADA'


-- total Bitcoin price per month

select  EXTRACT(
    YEAR FROM datum_razmerja
    ) AS year
, EXTRACT(
    MONTH FROM datum_razmerja
    ) AS month
, AVG(valutno_razmerje) as BTC_price
 from 	devizni_tecaj
where osnovna_valuta  = 'BTC'
and kotirajoca_valuta  = 'USD'
group by 1,2
order by 1,2

-- AUM per client

WITH t0 AS (SELECT *
            FROM transakcija
            WHERE uporabnik_id = 1)

SELECT SUM(COALESCE(v_kolicino * er2.valutno_razmerje, 0)) - SUM(COALESCE(iz_kolicine * er1.valutno_razmerje, 0)) as client_aum
FROM t0
         LEFT JOIN devizni_tecaj as er1 on er1.osnovna_valuta = iz_valute and er1.datum_razmerja = datum_cas	
         LEFT JOIN devizni_tecaj as er2 on er2.osnovna_valuta = v_valuto and er2.datum_razmerja = datum_cas	

