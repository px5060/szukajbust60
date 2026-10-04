"""Porównanie silnika JS (worker z index.html) z engine.py (sim + simA: powtórki BUST, okres sprawdzenia) na modelach z puli.
Uruchom:  python3 xcheck.py .. t50|t60"""
import json, re, subprocess, sys, pathlib, numpy as np, random
from engine import *
repo = pathlib.Path(sys.argv[1]); name = sys.argv[2]
html = (repo / 'index.html').read_text()
wsrc = re.search(r'<script id="wsrc" type="text/js-worker">(.*?)</script>', html, re.S).group(1)
pools = json.loads(re.search(r'const POOLS = (\{.*?\});\s', html).group(1))
seed = re.search(r"const MASTER_SEED = '(\d+)'", html).group(1)
al = ALPH[name]; random.seed(3)
codes = [seed[i:i+3] for i in range(0, len(seed), 3)] + random.choices(al, k=37)   # + 37 "nowych" kodów
X = np.array([al.index(c) for c in codes], np.int64)
bad = 0
for t, P in pools.items():
    y = np.array([c[TARGET_POS[t]] == '1' for c in al], np.uint8)
    mods = random.sample(P['pool'], 300)
    js = wsrc + f"""
setData({{AL:{json.dumps(al)},X:{json.dumps(X.tolist())},Y:{json.dumps(y.tolist())}}});
const R={{rules:[[200,5],[300,9],[400,11]],minCyc:100,minBust:3,maxClose:0,gap:2,split:0.65}};
console.log(JSON.stringify({json.dumps(mods, ensure_ascii=False)}.map(m=>{{const r=sim(m,R);return [r.nb,r.nw,r.nbu,r.pnl,r.k5,r.k5w,r.bs,r.ph,r.srow,r.wz,r.cnt,r.mg,r.sinceB,r.ci,r.bi,r.mgi,r.co,r.bo,r.mgo,r.zo,r.zb,r.cl,r.cli];}})));"""
    tmp = pathlib.Path(__import__('tempfile').gettempdir()) / 'xcheck_szbust.js'; tmp.parent.mkdir(parents=True, exist_ok=True)
    tmp.write_text(js.replace('onmessage =', 'const _om =').replace('postMessage', '(()=>0)'))
    p = subprocess.run(['node', str(tmp)], capture_output=True, text=True)
    if p.returncode: print(p.stderr[:2000]); sys.exit(1)
    out = json.loads(p.stdout)
    o = np.zeros(11, np.int64); oa = np.zeros(NA, np.int64)
    for m, r in zip(mods, out):
        a, la = table(m[1], al); b, lb = table(m[3], al)
        sim(a, la, b, lb, m[2], m[4], X, y, len(X), o)
        simA(a, la, b, lb, m[2], m[4], X, y, len(X), int(len(X) * 0.65), 2, oa)
        exp = list(o) + [oa[j] for j in (4, 5, 8, 9, 10, 11, 12, 13, 14, 15, 17, 18)]
        if exp != r: bad += 1; print('RÓŻNICA', m, exp, r)
    print(name, t, 'sprawdzono', len(mods), 'modeli, różnic:', bad)
