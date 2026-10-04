# SZUKAJ BUST — modele wersji A (BUST od razu po BUST-cie)

Appka = `../index.html` (repo osobne od RAZEM i SZUKAJ, własny adres). Szablon i narzędzia jak w `szukaj60`.

- **Silnik** = ten sam FSM co SZUKAJ (1:1 z silnikiem 1T z RAZEM): STEP (SERIA ×x albo UKŁAD) → TRIGGER → zakład na TRIGGER+offset,
  progresja trwała K8 (8, 8, 16, 32, 64, 128, 256, 512), kurs 3,0. `engine.py`: `sim` (bez zmian) i `simA` (ten sam przebieg plus
  odstępy między BUST-ami w cyklach, powtórki i okres sprawdzenia). `xcheck.py`: silnik JS ze strony = engine.py (sim i simA).
- **Powtórka** = BUST, po którym następny cykl też skończył się BUST-em (odstęp 1 cykl; `GAP = 2` w search.py,
  `gap` w konfiguracji strony — przygotowane na późniejsze rozszerzenie o kolejne cykle).
- **Nauka / sprawdzenie**: cykle zakończone na pierwszych 65% kodów / na ostatnich 35% (`SPLIT = 0.65`).
- **Kryteria** (domyślne): progi cykle/BUST jak w SZUKAJ, min. 150 cykli, min. 3 BUST-y, max 0 powtórek.
- **GRA**: modele w kryteriach tuż po BUST-cie (ostatni zakończony cykl = BUST).

## Pula z chmury

```
pip install numba numpy
python3 search.py t60 x1x ; python3 search.py t60 xx1
python3 build_szukaj.py t60          # → ../index.html
```

`search.py` liczy kilka milionów konfiguracji na bazie `seed_t60.txt` (+ `dopisane.txt`, jeśli jest), zapisuje pulę
(od 100 cykli, od 2 BUST-ów, max 2 powtórki, progi BUST +1; najlepsze wg powtórek, potem BUST/cykl, w przedziałach cykli)
i uczciwy test: modele wybrane tylko na nauce, wynik na sprawdzeniu (pole `test` w puli, widoczne w appce).
`--dolacz` dokłada modele z innym ziarnem: `python3 search.py t60 x1x 6000000 21 --dolacz`.
