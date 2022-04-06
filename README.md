
#  <img src="https://github.com/MatejRojec/Gamma/blob/main/logo.jpg" width="40" height="40"> 

## Opis

To je repozitori projekta pri predmetu Osnove podatkovnih baz. Naš projekt je namenje beleženju vseh sredstev uporabnika (AUM). Ko se uporabnik registrera dobi "Gama" račun, kjer ima možnost povezati svoje denarnice, odprte na različnih borzah. Skupno stanje se posodablja s trenutnimi deviznimi tečaji. Ko se uporabnik odloči za investicijo (ali katero koli drugo spremebo v denarnici), to ročno spremeni in vnese potrebne inormacije za spremembo. Tako se mu stanje posodobi in mu omogoča pregled in vrednost celotnega portfelija.

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
