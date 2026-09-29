import os, re, sys, posixpath
root = sys.argv[1]
os.chdir(root)
LINK = re.compile(r'\]\(([^)\s#]+)(?:#[^)]*)?\)')
TICK = re.compile(r'`((?:\.\./|\./)*(?:references|templates|examples|scripts)/[\w./-]+\.(?:md|php|js|sql|py))`')
broken = []
for base in ('skills', '00-meta-initialization'):
    for dp, _, fs in os.walk(base):
        for f in fs:
            if not f.endswith('.md'):
                continue
            p = os.path.join(dp, f).replace(os.sep, '/')
            t = open(p, encoding='utf-8', errors='ignore').read()
            for rx in (LINK, TICK):
                for m in rx.finditer(t):
                    tgt = m.group(1)
                    if '://' in tgt or tgt.startswith(('mailto:', '/', '<', '{')) or '*' in tgt or '<' in tgt:
                        continue
                    if not os.path.exists(posixpath.normpath(posixpath.join(dp.replace(os.sep, '/'), tgt))) and not os.path.exists(tgt):
                        broken.append(f'{p}: {tgt}')
print(len(broken))
if '-v' in sys.argv:
    for b in broken:
        print(b)
