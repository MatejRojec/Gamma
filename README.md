
#  <img src="https://github.com/MatejRojec/Gamma/blob/main/logo.jpg" width="20" height="20"> Gamma
Projekt pri predmetu osnove podatkovnih baz. 


## ER 
Povezava do [ER](https://github.com/MatejRojec/Gamma/blob/main/ER.pdf) diagrama.

## Struktura baze

Tu so naštete tabele ki jih bomo imeli v naši bazi:
- Uporabnik (ID uporabnika, ime, priimek, emšo, spol, datum rojstva, podjetje, datum registracije)
- Denarnica (Id denarnice, ID uporabnika, ID borze)
- Borza (ID borze, ime, vrsta)
- Stanje (sredstvo, vrednost sredstva, količina sredstva, ID denarnice, datum)
- Devizni tečaj (osnovna valuta, kotirajoča valuta, valutno razmerje)
- Transakcija (ID transakcije, iz valute, v valuto, iz količine, v količino, datum in čas, ID uporabnika)
- Tip naročila (vrsta naročila, podvrsta naročila, ID trasakcije)