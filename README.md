
#  <img src="https://github.com/MatejRojec/Gamma/blob/main/logo.jpg" width="40" height="40"> 

[![bottle.py](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/MatejRojec/Gamma/main?urlpath=proxy/8080/)

<p align="center">
  <img src="https://readme-typing-svg.herokuapp.com?lines=Gamma&center=true&width=500&height=50">
</p>

## Opis

To je repozitorij projekta pri predmetu Osnove podatkovnih baz. Naš projekt je namenjen beleženju vseh kripto sredstev uporabnika (AUM). Ko se uporabnik registrera dobi "Gama" račun, kjer ima možnost povezati svoje denarnice, odprte na različnih borzah. Skupno stanje se posodablja s trenutnimi deviznimi tečaji. Ko se uporabnik odloči za investicijo (ali katero koli drugo spremebo v denarnici), to ročno spremeni in vnese potrebne informacije za spremembo. Tako se mu stanje posodobi in mu omogoča pregled in vrednost celotnega portfelja.

## ER 
Povezava do [ER](https://github.com/MatejRojec/Gamma/blob/main/ER.pdf) diagrama.

## Struktura baze

Tu so naštete tabele, ki jih bomo imeli v naši bazi:
- Uporabnik (ID uporabnika, ime, priimek, emšo, spol, datum rojstva, podjetje, datum registracije)
- Denarnica (ID denarnice, ID uporabnika, ID borze)
- Borza (ID borze, ime, vrsta)
- Stanje (sredstvo, vrednost sredstva, količina sredstva, ID denarnice, datum)
- Devizni tečaj (osnovna valuta, kotirajoča valuta, valutno razmerje)
- Transakcija (ID transakcije, iz valute, v valuto, iz količine, v količino, datum in čas, ID uporabnika)
- Tip naročila (vrsta naročila, podvrsta naročila, ID trasakcije)
