"""M10-06 orphan-folder merge: move orphan skill-folder payloads next to the
consolidated reference file that replaced their SKILL.md, and repoint links.

Usage: python migrate.py [--apply]
Dry run prints the move plan and every token rewrite.
"""
import os, re, sys, shutil, posixpath, json

REPO = r'C:\wamp64\www\chwezi-dev-engine'
os.chdir(REPO)
APPLY = '--apply' in sys.argv

# orphan dir -> consolidated reference file (P). Payload moves to dirname(P)/<slug>/
MERGES = {
    'skills/architecture/api-error-handling': 'skills/architecture/api-design-first/references/api-error-handling.md',
    'skills/architecture/api-pagination': 'skills/architecture/api-design-first/references/api-pagination.md',
    'skills/architecture/microservices-architecture-models': 'skills/architecture/microservices-architecture/references/microservices-architecture-models.md',
    'skills/architecture/microservices-communication': 'skills/architecture/microservices-architecture/references/microservices-communication.md',
    'skills/architecture/orchestration-best-practices': 'skills/sdlc-meta/skill-composition-standards/references/orchestration-best-practices.md',
    'skills/backend-databases/mysql-administration': 'skills/backend-databases/mysql-operations/references/mysql-administration.md',
    'skills/backend-databases/mysql-advanced-sql': 'skills/backend-databases/mysql-engineering/references/mysql-advanced-sql.md',
    'skills/backend-databases/mysql-best-practices': 'skills/backend-databases/mysql-engineering/references/mysql-best-practices.md',
    'skills/backend-databases/mysql-data-modeling': 'skills/backend-databases/mysql-engineering/references/mysql-data-modeling.md',
    'skills/backend-databases/mysql-query-performance': 'skills/backend-databases/mysql-operations/references/mysql-query-performance.md',
    'skills/backend-databases/postgresql-administration': 'skills/backend-databases/postgresql-operations/references/postgresql-administration.md',
    'skills/backend-databases/postgresql-patterns': 'skills/backend-databases/postgresql-engineering/references/postgresql-patterns.md',
    'skills/backend-databases/postgresql-server-programming': 'skills/backend-databases/postgresql-engineering/references/postgresql-server-programming.md',
    'skills/devops-cloud/cicd-devsecops': 'skills/devops-cloud/cicd-pipelines/references/cicd-devsecops.md',
    'skills/devops-cloud/cicd-jenkins-debian': 'skills/devops-cloud/cicd-pipelines/references/cicd-jenkins-debian.md',
    'skills/devops-cloud/cicd-pipeline-design': 'skills/devops-cloud/cicd-pipelines/references/cicd-pipeline-design.md',
    'skills/devops-cloud/kubernetes-fundamentals': 'skills/devops-cloud/kubernetes-platform/references/kubernetes-fundamentals.md',
    'skills/devops-cloud/kubernetes-production': 'skills/devops-cloud/kubernetes-platform/references/kubernetes-production.md',
    'skills/devops-cloud/kubernetes-saas-delivery': 'skills/devops-cloud/kubernetes-platform/references/kubernetes-saas-delivery.md',
    'skills/devops-cloud/observability-platform': 'skills/devops-cloud/observability-monitoring/references/observability-platform.md',
    'skills/gis/gis-mapping': 'skills/gis/gis-platform-engineering/references/gis-mapping.md',
    'skills/gis/gis-maps-integration': 'skills/gis/gis-platform-engineering/references/gis-maps-integration.md',
    'skills/gis/gis-postgis-backend': 'skills/gis/gis-platform-engineering/references/gis-postgis-backend.md',
    'skills/languages/javascript-patterns': 'skills/languages/javascript-modern/references/javascript-patterns.md',
    'skills/languages/language-standards': 'skills/sdlc-meta/world-class-engineering/references/language-standards.md',
    'skills/languages/php-security': 'skills/languages/php-modern-standards/references/php-security.md',
    'skills/languages/python-saas-integration': 'skills/languages/python-modern-standards/references/python-saas-integration.md',
    'skills/languages/typescript-design-patterns': 'skills/languages/typescript-effective/references/typescript-design-patterns.md',
    'skills/languages/typescript-mastery': 'skills/languages/typescript-effective/references/typescript-mastery.md',
    'skills/sdlc-meta/e2e-testing': 'skills/sdlc-meta/advanced-testing-strategy/references/e2e-testing.md',
    'skills/sdlc-meta/plan-implementation': 'skills/sdlc-meta/implementation-status-auditor/references/plan-implementation.md',
    'skills/sdlc-meta/sdlc-design': 'skills/sdlc-meta/sdlc-documentation/references/sdlc-design.md',
    'skills/sdlc-meta/sdlc-planning': 'skills/sdlc-meta/sdlc-documentation/references/sdlc-planning.md',
    'skills/sdlc-meta/sdlc-testing': 'skills/sdlc-meta/sdlc-documentation/references/sdlc-testing.md',
    'skills/sdlc-meta/sdlc-user-deploy': 'skills/sdlc-meta/sdlc-documentation/references/sdlc-user-deploy.md',
    # no consolidated reference file: payload goes under the owning active skill's references
    'skills/finance-accounting/_chwezi-finance-engine-skeletons': 'skills/finance-accounting/accounting-engine/references/finance-engine-skeletons.md',
}

moves = {}  # old repo path -> new repo path (files)
for o, p in MERGES.items():
    slug = o.split('/')[-1]
    dest = posixpath.join(posixpath.dirname(p), slug.lstrip('_'))
    if os.path.exists(dest):
        sys.exit(f'destination exists: {dest}')
    for dp, _, fs in os.walk(o):
        for f in fs:
            old = os.path.join(dp, f).replace(os.sep, '/')
            moves[old] = dest + old[len(o):]

old_of = {v: k for k, v in moves.items()}
skillmd_to_p = {o + '/SKILL.md': p for o, p in MERGES.items()}

# All text files under active roots (post-move identity: path they will have after the move)
def all_md():
    for root in ('skills', '00-meta-initialization'):
        for dp, _, fs in os.walk(root):
            for f in fs:
                if f.endswith(('.md', '.php', '.js', '.sql')):
                    yield os.path.join(dp, f).replace(os.sep, '/')

TOKEN = re.compile(r'(?<![\w/.\-])((?:\.\.?/)*[\w\-]+(?:/[\w.\-]+)*\.(?:md|php|js|sql))(?![\w/\-])')

def exists_old(path):
    return os.path.isfile(path)

def resolve_old(token, old_file):
    """Return the repo path the token pointed at before the move, or None."""
    base = posixpath.dirname(old_file)
    cands = [posixpath.normpath(posixpath.join(base, token))]
    if token.startswith('skills/'):
        cands.insert(0, posixpath.normpath(token))
    # consolidated reference file P: bare references/ tokens meant the old skill dir
    for o, p in MERGES.items():
        if old_file == p:
            cands.append(posixpath.normpath(posixpath.join(o, token)))
    # category-less or wrong-depth forms: '<slug>/references/x.md', '../../<slug>/references/x.md'
    stripped = re.sub(r'^(\.\./|\./)+', '', token)
    for o in MERGES:
        slug = o.split('/')[-1]
        if stripped.startswith(slug + '/'):
            cands.append(o + stripped[len(slug):])
    for c in cands:
        if c in moves or c in skillmd_to_p:
            return c
    return None

changes = {}
report = []
for new_file in list(all_md()) + list(moves.values()):
    pass

files_to_scan = set()
for f in all_md():
    if f in moves:
        continue
    files_to_scan.add((f, f))  # (old, new)
for old, new in moves.items():
    if old.endswith(('.md', '.php', '.js', '.sql')):
        files_to_scan.add((old, new))

for old_file, new_file in sorted(files_to_scan):
    try:
        text = open(old_file, encoding='utf-8', newline='').read()
    except UnicodeDecodeError:
        continue
    new_text_parts = []
    last = 0
    changed = False
    for m in TOKEN.finditer(text):
        tok = m.group(1)
        if tok == 'SKILL.md':
            continue
        tgt_old = resolve_old(tok, old_file)
        if tgt_old is None:
            # a moved file's link to a non-moved existing file: recompute relative path
            if old_file != new_file and not tok.startswith('skills/'):
                abs_old = posixpath.normpath(posixpath.join(posixpath.dirname(old_file), tok))
                if os.path.isfile(abs_old) and abs_old not in moves:
                    tgt_new = abs_old
                else:
                    continue
            else:
                continue
        else:
            tgt_new = moves.get(tgt_old) or skillmd_to_p[tgt_old]
        if tok.startswith('skills/'):
            rep = tgt_new
        else:
            rep = posixpath.relpath(tgt_new, posixpath.dirname(new_file))
        if not tok.startswith('skills/') and posixpath.normpath(posixpath.join(posixpath.dirname(new_file), tok)) == tgt_new:
            continue
        if rep != tok:
            new_text_parts.append(text[last:m.start(1)])
            new_text_parts.append(rep)
            last = m.end(1)
            changed = True
            line = text.count('\n', 0, m.start()) + 1
            report.append(f'{new_file}:{line}: {tok} -> {rep}')
    if changed:
        new_text_parts.append(text[last:])
        changes[(old_file, new_file)] = ''.join(new_text_parts)

print(f'files to move: {len(moves)}; files with rewrites: {len(changes)}; token rewrites: {len(report)}')
for r in report:
    print('  ', r)
json.dump({'moves': moves, 'rewrites': report}, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'migrate-plan.json'), 'w'), indent=1)

if APPLY:
    for old, new in moves.items():
        os.makedirs(os.path.dirname(new), exist_ok=True)
        shutil.move(old, new)
    for (old_file, new_file), txt in changes.items():
        with open(new_file, 'w', encoding='utf-8', newline='') as fh:
            fh.write(txt)
    # remove now-empty orphan dirs (rmdir refuses non-empty)
    removed = []
    for o in MERGES:
        for dp, dns, fs in sorted(os.walk(o, topdown=False), key=lambda t: -len(t[0])):
            os.rmdir(dp)
            removed.append(dp.replace(os.sep, '/'))
    print('removed empty dirs:', len(removed))
    for r in removed:
        print('   rmdir', r)
