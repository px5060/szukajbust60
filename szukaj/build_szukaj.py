#!/usr/bin/env python3
"""Buduje ../index.html (appka SZUKAJ BUST — wersja A: BUST od razu po BUST-cie) z szukaj_template.html + seed_<t50|t60>.txt + pule pool_<t50|t60>_<cel>.json.
Uruchom w katalogu szukaj/:  python3 build_szukaj.py t50|t60"""
import json, re, sys, pathlib

HERE = pathlib.Path(__file__).resolve().parent
APPS = {
    't50': dict(title='T50 SZUKAJ BUST', app='t50', seedKey='t50razem_v1_added', razem='T50 RAZEM', razemUrl='/all50/?app=t50razem2', mid='t50-szukajbust-v1', targets=['x1x'],
                alph=[a + b + c for a in '01' for b in '01' for c in '01'], first='01x', maxUnion=3, seedFix={14676: '000'}),
    't60': dict(title='T60 SZUKAJ BUST', app='t60', seedKey='t60razem_v1_added', razem='T60 RAZEM', razemUrl='/all60/?app=t60razem', mid='t60-szukajbust-v1', targets=['x1x', 'xx1'],
                alph=[a + b + c for a in '0123' for b in '01' for c in '01'], first='0123x', maxUnion=2, seedFix={}),
}


def main():
    name = sys.argv[1]
    a = APPS[name]
    seed = re.sub(r'\D', '', (HERE / f'seed_{name}.txt').read_text())   # baza = MASTER_SEED appki RAZEM (od Nr 1)
    pools, tests = {}, {}
    for t in a['targets']:
        p = json.loads((HERE / f'pool_{name}_{t}.json').read_text())
        assert p['seedN'] <= len(seed) // 3
        pools[t] = {'seedN': p['seedN'], 'nCfg': p.get('nCfg', 0), 'pool': p['pool']}
        tests[t] = p.get('test', [])
        rules, minc, extra = p['rules'], p['minCyc'], {k: p[k] for k in ('minBust', 'maxClose', 'gap', 'split')}
    cfg = {k: a[k] for k in ('app', 'seedKey', 'razem', 'targets', 'alph', 'first', 'maxUnion', 'seedFix', 'razemUrl')}
    cfg.update(defRules=rules, minCyc=minc, test=tests, **extra)
    html = (HERE / 'szukaj_template.html').read_text()
    ver = re.search(r"const APP_VER = '([^']+)'", html).group(1)
    html = (html.replace('__VER__', ver).replace('__TITLE__', a['title']).replace('__RAZEM__', a['razem']).replace('__SEED__', seed)
                .replace('__CFG__', json.dumps(cfg, ensure_ascii=False))
                .replace('__POOLS__', json.dumps(pools, ensure_ascii=False, separators=(',', ':'))))
    (HERE.parent / 'index.html').write_text(html)
    # manifest: osobna appka pod własnym adresem (…/szukajNN/), niezależna od RAZEM
    man = {'id': a['mid'], 'name': a['title'] + ' — modele po BUST-cie (wersja A)', 'short_name': a['title'],
           'start_url': './', 'scope': './', 'display': 'standalone', 'orientation': 'portrait',
           'background_color': '#12151c', 'theme_color': '#1b1f2a',
           'icons': [{'src': f'szukaj-{n}.png', 'sizes': f'{n}x{n}', 'type': 'image/png', 'purpose': 'any'} for n in (192, 512)]}
    # SW: nawigacje zawsze z sieci (bez starej wersji z pamięci)
    (HERE.parent / 'szukaj-sw.js').write_text(
        "// SZUKAJ BUST: nawigacje zawsze z sieci (bez starej wersji z pamięci)\n"
        "self.addEventListener('install', () => self.skipWaiting());\n"
        "self.addEventListener('activate', e => e.waitUntil(self.clients.claim()));\n"
        "self.addEventListener('fetch', e => {\n"
        "  if (e.request.mode !== 'navigate') return;\n"
        "  e.respondWith(fetch(e.request.url, { cache: 'no-store' }).catch(() => fetch(e.request)));\n"
        "});\n")
    (HERE.parent / 'szukaj.webmanifest').write_text(json.dumps(man, ensure_ascii=False, indent=1))
    print('zapisano ../index.html', len(html) // 1024, 'KB;', {t: len(p['pool']) for t, p in pools.items()})


if __name__ == '__main__':
    main()
