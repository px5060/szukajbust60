"""SZUKAJ BUST — szukanie puli modeli wersji A (dużo cykli, mało BUST-ów, BUST-y nigdy blisko siebie) na całej bazie (seed_<t50|t60>.txt + opcjonalnie szukaj/dopisane.txt).
Uruchom w katalogu szukaj/:  python3 search.py t50|t60 x1x|xx1 [n_konfiguracji] [ziarno] [--dolacz]   (wymaga: pip install numba numpy)
Potem:                        python3 build_szukaj.py t50|t60   → ../index.html"""
import sys, json, itertools, time, re, pathlib, numpy as np
from engine import *

HERE = pathlib.Path(__file__).resolve().parent


def seed_codes():
    """Baza (seed_<t50|t60>.txt = MASTER_SEED appki RAZEM od Nr 1) + kody z dopisane.txt (same cyfry, dowolne odstępy)."""
    name = 't50' if (HERE / 'seed_t50.txt').exists() else 't60'
    s = re.sub(r'\D', '', (HERE / f'seed_{name}.txt').read_text())
    f = HERE / 'dopisane.txt'
    if f.exists():
        s += re.sub(r'\D', '', f.read_text())
    return [s[i:i + 3] for i in range(0, len(s) - len(s) % 3, 3)]


RULES = [(200, 5), (300, 9), (400, 11), (None, 11)]   # None = ponad ostatni próg (bez górnej granicy)
MIN_CYC = 100       # domyślne min. cykli w appce (przedziały 100–200 · 201–300 · 301–400 · 401+, jak w SZUKAJ)
MIN_BUST = 3        # domyślne min. BUST-ów (1–2 BUST-y mało mówią o powtórkach)
GAP = 2             # powtórka = następny BUST po mniej niż GAP cyklach; 2 = BUST zaraz po BUST-cie (cykl po cyklu)
MAX_CLOSE = 0       # domyślnie 0 powtórek w historii (BUST nigdy od razu po BUST-cie)
SPLIT = 0.65        # okres sprawdzenia = ostatnie 35% kodów
POOL_CYC = 100      # do puli: od 100 cykli
POOL_BUST = 2       # do puli: od 2 BUST-ów
POOL_CLOSE = 2      # do puli: max 2 powtórki (appka filtruje wg ustawienia)
MARGIN = 1          # w puli też modele o 1 BUST ponad limit (mogą wejść z nowymi kodami); appka filtruje ściśle
TAKE = [(401, 10**9, 1000), (100, 200, 2500), (201, 300, 3000), (301, 400, 1500)]   # pula ~8000 modeli


def specs(name):
    al = ALPH[name]
    pats = [a + b + c for a in FIRST[name] for b in '01x' for c in '01x' if a + b + c != 'xxx']
    step = []
    for r in (1, 2, 3) if name == 't50' else (1, 2):
        for U in itertools.combinations(al, r):
            step.append(('SERIA', '∪'.join(U)))
    step += [('UKŁAD', p + ' → ' + q) for p in pats for q in pats]
    trig = pats + [p + ' → ' + q for p in pats for q in pats]
    return al, step, trig


def tabs(preds, al):
    T = np.zeros((len(preds), 3, len(al)), np.uint8); L = np.zeros(len(preds), np.int64)
    for k, p in enumerate(preds):
        T[k], L[k] = table(p, al)
    return T, L


def lim_of(cyc):
    lim = np.full(len(cyc), -1)
    for mc, mb in reversed(RULES):
        lim[cyc <= mc if mc is not None else cyc >= 0] = mb
    return lim


def main():
    name, target = sys.argv[1], sys.argv[2]
    n = int(sys.argv[3]) if len(sys.argv) > 3 else 6_000_000
    codes = seed_codes()
    al, step, trig = specs(name)
    X = np.array([al.index(c) for c in codes], np.int64)
    y = np.array([c[TARGET_POS[target]] == '1' for c in al], np.uint8)
    STAB, SL = tabs([s for _, s in step], al); TTAB, TL = tabs(trig, al)
    seed = int(sys.argv[4]) if len(sys.argv) > 4 else 7
    rng = np.random.default_rng(seed)
    a = rng.integers(0, len(step), n); b = rng.integers(0, len(trig), n); off = rng.integers(1, 8, n)
    ser = np.array([t == 'SERIA' for t, _ in step])[a]
    x = np.where(ser, rng.integers(1, 6, n), 1)
    cfg = np.unique(np.stack([a, b, x, off], 1).astype(np.int64), axis=0)
    split = int(len(X) * SPLIT)
    OUT = np.zeros((len(cfg), NA), np.int64)
    t = time.time(); run_cfgA(STAB, SL, TTAB, TL, cfg, X, y, len(X), split, GAP, OUT)
    cyc = OUT[:, 1] + OUT[:, 2]; bu = OUT[:, 2]; cl = OUT[:, 17]
    lim = lim_of(cyc)
    ok = (cyc >= POOL_CYC) & (lim >= 0) & (bu <= lim + MARGIN) & (bu >= POOL_BUST) & (cl <= POOL_CLOSE)
    strict = (cyc >= MIN_CYC) & (lim >= 0) & (bu <= lim) & (bu >= MIN_BUST) & (cl <= MAX_CLOSE)
    print(f'{name} {target}: {len(cfg):,} konfiguracji w {time.time()-t:.0f}s; wersja A (domyślne) {strict.sum():,} , do puli {ok.sum():,}')
    for lo, hi in [(100, 200), (201, 300), (301, 400), (401, 10**9)]:
        g = strict & (cyc >= lo) & (cyc <= hi); print(f'   cykle {lo}-{hi}: {g.sum():,}')

    # test uczciwy: cechy z pierwszych 65% kodów (nauka), wynik na ostatnich 35% (sprawdzenie):
    # BUST w sprawdzeniu → czy następny cykl też skończył się BUST-em (powtórka)
    ci, bi, cli, zo, zb = OUT[:, 8], OUT[:, 9], OUT[:, 18], OUT[:, 14], OUT[:, 15]
    base = (ci >= int(POOL_CYC * SPLIT)) & (bi >= 1)
    test = []
    for lbl, sel in [('wszystkie modele', base), (f'nauka: min {MIN_BUST} BUST, max {MAX_CLOSE} powtórek', base & (bi >= MIN_BUST) & (cli <= MAX_CLOSE)),
                     (f'nauka: min {MIN_BUST} BUST, max 1 powtórka', base & (bi >= MIN_BUST) & (cli <= 1)), (f'nauka: min 6 BUST, 0 powtórek', base & (bi >= 6) & (cli == 0))]:
        rec = dict(label=lbl, models=int(sel.sum()), zones=int(zo[sel].sum()), broken=int(zb[sel].sum()))
        test.append(rec)
        print(f'   test {lbl}: modeli {rec["models"]:,}, BUST-y w sprawdzeniu {rec["zones"]:,}, od razu kolejny BUST {100*rec["broken"]/max(rec["zones"],1):.1f}%')

    # pula warstwowa: w każdym przedziale cykli najlepsze wg powtórek, potem BUST/cykl
    old = HERE / f'pool_{name}_{target}.json'
    keep = json.loads(old.read_text())['pool'] if old.exists() and '--dolacz' in sys.argv else []
    idx = []
    for lo, hi, take in TAKE:
        g = np.where(ok & (cyc >= lo) & (cyc <= hi))[0]
        idx += list(g[np.lexsort((bu[g] / cyc[g], cl[g]))][:take])
    pool = []
    for k in idx:
        t_, s_ = step[cfg[k, 0]]
        pool.append([t_[0], s_, int(cfg[k, 2]), trig[cfg[k, 1]], int(cfg[k, 3])])
    seen = {json.dumps(m, ensure_ascii=False) for m in pool}
    pool += [m for m in keep if json.dumps(m, ensure_ascii=False) not in seen]
    json.dump({'name': name, 'target': target, 'seedN': len(codes), 'rules': RULES, 'minCyc': MIN_CYC, 'minBust': MIN_BUST,
               'gap': GAP, 'maxClose': MAX_CLOSE, 'split': SPLIT, 'nCfg': int(len(cfg)), 'test': test, 'pool': pool},
              open(HERE / f'pool_{name}_{target}.json', 'w'), ensure_ascii=False, separators=(',', ':'))
    print('   pula zapisana:', len(pool))


if __name__ == '__main__':
    main()
