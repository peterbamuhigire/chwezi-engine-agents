import json, os
from collections import Counter
S = os.path.dirname(os.path.abspath(__file__))
mv = json.load(open(os.path.join(S, 'migrate-plan.json')))['moves']
def load(p):
    return [l.rstrip('\n') for l in open(os.path.join(S, p)).readlines()[1:]]
b = load('lc-before.txt'); a = load('lc-after.txt')
cb = Counter((mv.get(l.split(': ', 1)[0], l.split(': ', 1)[0]), l.split(': ', 1)[1]) for l in b)
ca = Counter(tuple(l.split(': ', 1)) for l in a)
new = ca - cb
print('broken after, not broken before (after mapping old->new path):', sum(new.values()))
for k in new:
    print('  ', k)
print('fixed:', sum((cb - ca).values()))
