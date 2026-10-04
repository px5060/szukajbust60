# T60 SZUKAJ BUST

Trzecia appka z rodziny SZUKAJ dla ciągu **Test60** (BET x1x i xx1). Ten sam silnik, wygląd, zakładki **GRA · TABELA · MOJE · SZUKAJ**
i wspólne kody z **T60 RAZEM**. Osobna appka: własny adres, ikona (czerwona, „B60”) i instalacja.

Adres: **https://px5060.github.io/szukajbust60/**

## Wersja A: BUST od razu po BUST-cie

Szuka modeli STEP → TRIGGER → zakład z dużą liczbą cykli i małą liczbą BUST-ów, w których **BUST nie przychodził od razu po BUST-cie**
(cykl zaraz po BUST-cie kończył się WIN).

- **GRA** pokazuje modele w kryteriach, które są **tuż po BUST-cie**: ich ostatni cykl skończył się BUST-em, teraz trwa następny cykl
  Lista kroków **k2–k7** (domyślnie k5–k7, jak w SZUKAJ): widać tylko modele po BUST-cie na wybranych krokach, wchodzisz od tego kroku do WIN albo kroku 8. Na karcie: kiedy był BUST, krok, stan (GRA / zakład ustawiony / STEP / czekam),
  historia (cykle, BUST-y, co ile cykli BUST, ile razy BUST od razu po BUST-cie, ile razy WIN po BUST-cie) i **Sprawdzenie**.
- **Sprawdzenie** = ostatnie 35% kodów: cykle, BUST-y i ile razy w tym okresie BUST przyszedł od razu po BUST-cie.
  Zakładka SZUKAJ ma tabelę zbiorczą „Czy brak powtórek się utrzymuje?” i uczciwy test z chmury
  (modele wybrane tylko na pierwszych 65% kodów, wynik na ostatnich 35%).
- **Kryteria** (zakładka SZUKAJ, do zmiany): do 200 cykli max 5 BUST, do 300 max 9, do 400 max 11, ponad 400 max 11, min. 150 cykli,
  min. 3 BUST-y (1–2 BUST-y mało mówią o powtórkach), max 0 BUST-ów od razu po BUST-cie.
- **TABELA**: etykiety modelu na ciągu kodów. Przy BUST-cie widać, ile cykli minęło od poprzedniego BUST-u; „BUST OD RAZU PO BUST-CIE” jest wyróżniony.
  W kolumnie GRA zaznaczone są zakłady w cyklach po BUST-cie.
- **MOJE**: „Gram ten model” śledzi grę do WIN albo kroku 8 (osobne od MOJE w SZUKAJ).
- **Kody** wspólne z T60 RAZEM (ta sama domena, klucz `t60razem_v1_added`). Import pliku eksportu z RAZEM: zakładka SZUKAJ → Import kodów.

### Wynik testu (baza z repo)

Po BUST-cie kolejny BUST od razu w następnym cyklu, okres sprawdzenia: T60 x1x: 5,4% i 5,3%; T60 xx1: 5,4% i 5,4%.
Czyli tyle, ile wynosi zwykła częstość BUST-u na cykl. Brak powtórek w przeszłości nie zmniejszył tego ryzyka.

## Pliki

```
index.html            appka (generowana — nie edytować ręcznie)
szukaj.webmanifest    PWA (zakres ./)
szukaj-sw.js          service worker: strona zawsze z sieci
szukaj-192/512.png    ikony
szukaj/               narzędzia: silnik, szukanie puli, budowanie (szukaj/README.md)
```

Przebudowa: `cd szukaj && python3 build_szukaj.py t60`. Nowa pula (wymaga numba): `python3 search.py t60 x1x ; python3 search.py t60 xx1`, potem build.
Baza ciągu: `szukaj/seed_t60.txt` (MASTER_SEED z T60 RAZEM), dopisane kody PC: `szukaj/dopisane.txt`.
