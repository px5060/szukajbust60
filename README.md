# T60 SZUKAJ BUST

Trzecia appka z rodziny SZUKAJ dla ciągu **Test60** (BET x1x i xx1). Ten sam silnik, wygląd, zakładki **GRA · TABELA · MOJE · SZUKAJ**
i wspólne kody z **T60 RAZEM**. Osobna appka: własny adres, ikona (czerwona, „B60”) i instalacja.

Adres: **https://px5060.github.io/szukajbust60/**
- **MOJE ZAKŁADY** (jak w RAZEM): w oknie statystyk modelu (przytrzymaj kartę albo wiersz tabeli) zapis zakładu zagranego naprawdę — Nr wiersza, krok, kwota; wynik z tabeli modelu (✔ WIN = +2 × stawka, ✗ przegrany, czeka). W zakładce MOJE podsumowanie (model · zakł. · kroki · postawione · wynik, Σ, według kroku) i lista wszystkich zakładów. Dotknięcie zakładu → TABELA modelu na wierszu zakładu.

## Wersja A: BUST od razu po BUST-cie

Szuka modeli STEP → TRIGGER → zakład z dużą liczbą cykli i małą liczbą BUST-ów, w których **BUST nie przychodził od razu po BUST-cie**
(cykl zaraz po BUST-cie kończył się WIN).

- **GRA** pokazuje modele w kryteriach, które są **tuż po BUST-cie**: ich ostatni cykl skończył się BUST-em, teraz trwa następny cykl
  Lista kroków **k1–k7** (domyślnie k5–k7, jak w SZUKAJ): widać tylko modele po BUST-cie, które są już po TRIGGERZE (GRA na następnym albo zakład ustawiony za kilka wierszy), na wybranych krokach, wchodzisz od tego kroku do WIN albo kroku 8. Na karcie: kiedy był BUST, krok, stan (GRA / zakład ustawiony / STEP / czekam),
  historia (cykle, BUST-y, co ile cykli BUST, ile razy BUST od razu po BUST-cie, ile razy WIN po BUST-cie) i **Sprawdzenie**.
- **Sprawdzenie** = ostatnie 35% kodów: cykle, BUST-y i ile razy w tym okresie BUST przyszedł od razu po BUST-cie.
  Zakładka SZUKAJ ma tabelę zbiorczą „Czy brak powtórek się utrzymuje?” i uczciwy test z chmury
  (modele wybrane tylko na pierwszych 65% kodów, wynik na ostatnich 35%).
- **Kryteria** (zakładka SZUKAJ, do zmiany): do 200 cykli max 5 BUST, do 300 max 9, do 400 max 11, ponad 400 max 11, min. 100 cykli (przedziały 100–200 · 201–300 · 301–400 · 401+, w każdym „od X” i „max Y” BUST),
  min. 3 BUST-y (1–2 BUST-y mało mówią o powtórkach), max 0 BUST-ów od razu po BUST-cie.
- **TABELA**: etykiety modelu na ciągu kodów. Przy BUST-cie widać, ile cykli minęło od poprzedniego BUST-u; „BUST OD RAZU PO BUST-CIE” jest wyróżniony.
  W kolumnie GRA zaznaczone są zakłady w cyklach po BUST-cie.
- **MOJE**: „Gram ten model” śledzi grę do WIN albo kroku 8 (osobne od MOJE w SZUKAJ).
- **Tylko pula z chmury**: szukania w telefonie nie ma, więc telefon, appka i PC pokazują te same modele. Pulę aktualizuje `szukaj/search.py` na nowym ciągu, potem nowa wersja appki.
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
