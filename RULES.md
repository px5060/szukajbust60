# RULES — rodzina aplikacji SZUKAJ (stan ustaleń)

Ten plik jest wspólny dla repo: `szukaj50`, `szukaj60`, `szukaj50plus`, `szukaj60plus`, `szukajbust50`, `szukajbust60`.
Zapisuje reguły i ustalenia z rozmów, żeby przetrwały streszczenie (kompakcję) kontekstu i nowe sesje.

## Sposób pracy

- Rozmowa po polsku, prosto, bez żargonu. Symbole z `x` (np. `x1x`, `00x`) zostają — użytkownik je rozumie.
- **PR scalany dopiero po słowie „scal”** od użytkownika. Nigdy samodzielnie.
- Gałąź robocza: `ccr-70037d68-ntwxyk` (po scaleniu: odtworzyć od `origin/main`).
- Edytuje się `szukaj/szukaj_template.html`, potem build: `cd szukaj && python3 build_szukaj.py t50|t60` → `../index.html`.
  Para 50/60 ma identyczny szablon — zmiana w jednym = skopiować do drugiego (BUST i SZUKAJ+ mają własne szablony).
- Przy każdej zmianie podbić `APP_VER` (nagłówek pokazuje wersję; appka sama proponuje odświeżenie).
- Zmiana „dla wszystkich SZUKAJ” = SZUKAJ 50/60 + SZUKAJ+ 50/60 (+ BUST 50/60, jeśli funkcja tam istnieje).
- Test przed PR: Playwright z Chromium (`/opt/pw-browsers/chromium`), sprawdzić brak błędów JS i wynik na danych.
- Adresy: `https://px5060.github.io/<repo>/`. Kody wspólne z RAZEM (`t50razem_v1_added` / `t60razem_v1_added`).
- RAZEM: T50 = repo `all50` (src + build.py → `index.html`, `pages/t50razem/` kopiowane do repo `t50razem`), T60 = repo `all60` (sam `index.html`, appki jako JSON w `APPS = […]`).

## Model i gra

- Model: STEP (SERIA ×x albo UKŁAD p→q) → TRIGGER → zakład na wierszu TRIGGER + offset. SZUKAJ+: dodatkowo STEP2 i TRIGGER ×2/×3.
- Cel: T50 `x1x`; T60 `x1x` lub `xx1`. Kurs 3,0. WIN = +2 × stawka.
- Progresja K8 trwała: 8 · 8 · 16 · 32 · 64 · 128 · 256 · 512 zł. WIN → krok 1. **BUST = przegrany krok 8 (512 zł bez trafienia)** → krok 1.
- **Cykl** = gra modelu do WIN albo BUST (to NIE są wiersze; jeden cykl trwa różną liczbę wierszy).
- Kryteria (domyślne): do 200 cykli max 5 BUST, do 300 max 9, do 400 max 11, ponad 400 max 11, min. 100 cykli.
- Pula modeli liczona w chmurze (`search.py`); w telefonie każdy kod przelicza całą pulę. Szukanie w telefonie wyłączone.

## Ekran GRA (SZUKAJ / SZUKAJ+)

- „krok:” — **k1 8 zł, k2 8 zł, 16 … 512 zł** (k1…k8); domyślnie 64/128/256. Pokazuje modele po TRIGGERZE na wybranych krokach.
- „cykle:” — przedziały 100–200 · 201–300 · 301–400 · ★ 401+ oraz **BUST**.
- **BUST** (lista) — tylko modele, których **ostatni zakończony cykl to BUST i od BUST-u nie było WIN** (po WIN model znika).
  Filtrowana po krokach jak przedziały (zaraz po BUST-cie model jest na k1).
  - „poprz. BUST: **≤ 20 cykli**” / „**21–40 cykli**” — odstęp **w cyklach** od poprzedniego BUST-u modelu (model z jednym BUST-em nie wchodzi).
  - „**po BUST**” — model w cyklu zaraz po BUST-cie, GRA na następnym wierszu albo zakład za 2–3 wiersze.
  - Model z zakładem (na kroku) ma pod wierszem BUST-u kartę jak pozostałe (pomarańczowa przy GRA na następnym).
- Biało-czerwona ramka karty = model w cyklu zaraz po BUST-cie (`sinceB === 0`).
- Znaczki jak w RAZEM: **pomarańczowy** = ile modeli gra na następnym wierszu, **żółty** = GRA za 2–3 wiersze
  (przycisk BUST, „moje · busty”, dolny przycisk MOJE).

## MOJE

- „▶ moje” na GRA: podzakładki **gry** · **busty** · **w grze** (w BUST: „▶ MOJE”: gry · w grze).
- **gry** — modele dodane „▶ Gram ten model”, śledzone do WIN albo kroku 8.
- **busty** — BUST-y moich modeli od dodania; **zostają po usunięciu modelu z MOJE** (✕ usuwa wpis); znikają po WIN modelu.
- **w grze** — zapisane zakłady (MOJE ZAKŁADY): postawione i czekające na wynik + przegrane, gdy progresja modelu trwa.
- Dolny przycisk MOJE: żółty = za ile wierszy GRA w moich modelach, pomarańczowy = ile gra na następnym; świeci, gdy jest zakład.

## TABELA i inne

- TABELA chronologicznie; dotknięcie wiersza → łańcuch STEP/TRIGGER, ponowne → zamyka; przytrzymanie → STATYSTYKI.
- Dotknięcie wiersza WIN/przegrana → okienko z wynikami wszystkich modeli na tym wierszu.
- Po wpisaniu kodu na wierszu gry: okienko WIN/PRZEGRANA, przejście do tabeli i rozbłysk wiersza.
- Statystyki: pasek „Ostatnie N cykli” to cykle (W krok / BUST), nie wiersze.
- RAZEM: okno „Statystyki modelu” musi mieć białą czcionkę w każdej tabeli (TRÓJKA, 2-SLOT, MIX3 miały czarną — poprawione);
  T60 MIX3 → STATY w układzie TRÓJKI (T50Stat).

## Aplikacja MOJE (repo `moje`, adres `/moje/`)

- Zbiera MOJE (modele, które gram) i MOJE ZAKŁADY ze wszystkich SZUKAJ / SZUKAJ+ / BUST, T50 i T60 — czyta wspólną pamięć telefonu, nic nie kopiuje.
- Przycisk w oknie statystyk SZUKAJ / SZUKAJ+ „⇢ Gram — dodaj do MOJE i otwórz” zastąpił dawne „Dodaj do RAZEM — zakładka SZUKAJ”.
- Poza tym przyciskiem aplikacji źródłowych **nie zmieniamy** pod MOJE.
- Wpis kodów w MOJE: przy każdej tabeli ostatni kod i kiedy wpisany („5 minut temu”, „2 dni temu”).
