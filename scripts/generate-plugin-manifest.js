#!/usr/bin/env node
/**
 * generate-plugin-manifest.js — shared, engine-agnostic version.
 *
 * Regenerates <engine>/.claude-plugin/plugin.json from that engine's actual
 * skill tree, using the explicit-path-array form documented in the ECC audit
 * (installation report, §3, "Fallback A"): every SKILL.md's containing
 * directory is listed individually, so the Claude Code plugin loader never
 * has to walk an arbitrary, unverified nesting depth.
 *
 * Handles the three skill-root shapes found across the Chwezi engines:
 *   - skills/<skill>/SKILL.md                      (flat)          e.g. digital-research-engine
 *   - skills/<category>/<skill>/SKILL.md            (one level)     e.g. business-plan, proposal, website, social-media, chwezi-dev-engine
 *   - skills/<NN-category>/<NN-skill>/SKILL.md      (one level)     e.g. chwezi-design-engine, chwezi-sdlc-documentation (roots differ — see --root)
 *   - <NN-area>/SKILL.md at the repo root, no skills/ dir           e.g. linux-skills (use --root .)
 *
 * Follows the constraints in ECC's .claude-plugin/PLUGIN_SCHEMA_NOTES.md:
 *   - "version" is mandatory
 *   - "skills" must be an array
 *   - NEVER add an "agents" field (auto-discovered by convention)
 *   - NEVER add a "hooks" field for the standard hooks/hooks.json
 *   - keep "mcpServers": {} as an explicit opt-out
 *
 * Usage:
 *   node generate-plugin-manifest.js --engine <path> [--root <skills-subdir>] [--check] [--exclude <name,name>]
 *   node generate-plugin-manifest.js --check-marketplace [--workspace-root <dir>] [--suite-root <dir>]
 *
 * --check-marketplace (read-only, M10-02-T09) compares the leading "N skills"
 * integer of every marketplace description with the target plugin.json
 * skills[].length, for the suite marketplace (this package) and for each
 * catalogued engine's own marketplace.json, and asserts that every relative
 * `source` path exists. Exit 0 consistent, 1 drift, 3 NOT_ASSESSED only
 * (a sibling engine checkout is missing; never reported as a pass).
 *
 * Examples:
 *   node generate-plugin-manifest.js --engine ../../digital-research-engine
 *   node generate-plugin-manifest.js --engine ../../chwezi-sdlc-documentation --exclude "%SystemDrive%,projects,docs,references,templates,engine,book-extractions"
 *   node generate-plugin-manifest.js --engine ../../linux-skills --root . --exclude "docs,scripts,templates,tests,commands,meta,notes,prompts"
 */

'use strict';

const fs = require('fs');
const path = require('path');

function parseArgs(argv) {
  const args = { root: 'skills', exclude: '_TEMPLATE,node_modules,.git', check: false };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--engine') args.engine = argv[++i];
    else if (a === '--root') args.root = argv[++i];
    else if (a === '--exclude') args.exclude = argv[++i];
    else if (a === '--check') args.check = true;
    else if (a === '--version') args.version = argv[++i];
    else if (a === '--check-marketplace') args.checkMarketplace = true;
    else if (a === '--workspace-root') args.workspaceRoot = argv[++i];
    else if (a === '--suite-root') args.suiteRoot = argv[++i];
  }
  if (args.checkMarketplace) return args;
  if (!args.engine) {
    console.error('Usage: node generate-plugin-manifest.js --engine <path> [--root <dir>] [--check] [--exclude a,b,c]');
    process.exit(2);
  }
  return args;
}

/**
 * A directory can simultaneously BE a skill (own SKILL.md) and CONTAIN
 * further nested skills one or more levels down — e.g.
 * proposal-skills/skills/profiles-sectors/{SKILL.md, sectors/<name>/SKILL.md}.
 * So "found a SKILL.md here" must never stop the recursion — it only adds
 * this directory to the result and continues into every subdirectory
 * regardless. An earlier version of this script stopped at the first
 * SKILL.md per branch and silently dropped every skill nested beneath it;
 * verified against proposal-skills, where it missed 17 of 111 real skills.
 */
function findSkillDirs(dir, excludeSet, out) {
  let entries;
  try {
    entries = fs.readdirSync(dir, { withFileTypes: true });
  } catch (e) {
    return out;
  }
  if (fs.existsSync(path.join(dir, 'SKILL.md'))) {
    out.push(dir);
  }
  for (const entry of entries) {
    if (!entry.isDirectory()) continue;
    if (entry.name.startsWith('.')) continue;
    if (excludeSet.has(entry.name)) continue;
    findSkillDirs(path.join(dir, entry.name), excludeSet, out);
  }
  return out;
}

/**
 * Read the catalogued engines (repository name -> checkout path) from
 * catalog/engines.yaml without a YAML dependency. The file is a flat list of
 * "- id:" blocks with "repository:" and "path:" scalars.
 */
function readCatalog(suiteRoot) {
  const file = path.join(suiteRoot, 'catalog', 'engines.yaml');
  if (!fs.existsSync(file)) return [];
  const engines = [];
  let current = null;
  for (const line of fs.readFileSync(file, 'utf8').split(/\r?\n/)) {
    const id = line.match(/^\s*-\s+id:\s*"?([^"\s]+)"?/);
    if (id) { current = { id: id[1] }; engines.push(current); continue; }
    const kv = current && line.match(/^\s+(repository|path):\s*"?([^"\s]+)"?\s*$/);
    if (kv) current[kv[1]] = kv[2];
  }
  return engines.filter((e) => e.path);
}

function leadingCount(description) {
  const m = /^(\d+)\s+skills\b/.exec(description || '');
  return m ? Number(m[1]) : null;
}

function pluginSkillCount(pluginRoot) {
  const file = path.join(pluginRoot, '.claude-plugin', 'plugin.json');
  if (!fs.existsSync(file)) return { missing: true };
  const manifest = JSON.parse(fs.readFileSync(file, 'utf8'));
  return { count: Array.isArray(manifest.skills) ? manifest.skills.length : null };
}

function checkMarketplaceFile(label, marketplaceFile, repoRoot, resolveUrl, out) {
  const marketplace = JSON.parse(fs.readFileSync(marketplaceFile, 'utf8'));
  for (const entry of marketplace.plugins || []) {
    let target = null;
    if (typeof entry.source === 'string') {
      target = path.resolve(repoRoot, entry.source);
      if (!fs.existsSync(target)) {
        out.drift.push(`${label}: ${entry.name}: relative source ${entry.source} does not exist`);
        continue;
      }
    } else if (entry.source && entry.source.url) {
      target = resolveUrl(entry.source.url);
      if (!target) { out.notAssessed.push(`${label}: ${entry.name}: no local checkout for ${entry.source.url}`); continue; }
    } else {
      out.drift.push(`${label}: ${entry.name}: source is neither a relative path nor a url`);
      continue;
    }
    const stated = leadingCount(entry.description);
    if (stated === null) { out.ok.push(`${label}: ${entry.name}: no count in description (not checked)`); continue; }
    const actual = pluginSkillCount(target);
    if (actual.missing) { out.drift.push(`${label}: ${entry.name}: ${path.relative(repoRoot, target) || '.'}/.claude-plugin/plugin.json missing`); continue; }
    if (actual.count === null) { out.ok.push(`${label}: ${entry.name}: plugin.json skills is not a list (not checked)`); continue; }
    if (stated !== actual.count) out.drift.push(`${label}: ${entry.name}: description says ${stated} skills, plugin.json lists ${actual.count}`);
    else out.ok.push(`${label}: ${entry.name}: ${stated} skills`);
  }
}

function checkMarketplace(args) {
  const suiteRoot = path.resolve(args.suiteRoot || path.join(__dirname, '..'));
  const workspace = path.resolve(args.workspaceRoot || path.join(suiteRoot, '..'));
  const catalog = readCatalog(suiteRoot);
  const byRepo = new Map(catalog.map((e) => [e.repository || e.path, e.path]));
  const resolveUrl = (url) => {
    const repo = url.replace(/\/+$/, '').split('/').pop().replace(/\.git$/, '');
    const folder = byRepo.get(repo) || repo;
    const dir = path.join(workspace, folder);
    return fs.existsSync(dir) ? dir : null;
  };
  const out = { ok: [], drift: [], notAssessed: [] };
  const suiteFile = path.join(suiteRoot, '.claude-plugin', 'marketplace.json');
  if (fs.existsSync(suiteFile)) checkMarketplaceFile('suite', suiteFile, suiteRoot, resolveUrl, out);
  else out.drift.push(`suite: ${suiteFile} missing`);
  for (const engine of catalog) {
    const root = path.join(workspace, engine.path);
    if (!fs.existsSync(root)) { out.notAssessed.push(`${engine.path}: sibling checkout missing`); continue; }
    const file = path.join(root, '.claude-plugin', 'marketplace.json');
    if (fs.existsSync(file)) checkMarketplaceFile(engine.path, file, root, resolveUrl, out);
  }
  for (const line of out.ok) console.log(`ok     ${line}`);
  for (const line of out.notAssessed) console.log(`NOT_ASSESSED ${line}`);
  for (const line of out.drift) console.error(`DRIFT  ${line}`);
  console.log(`marketplace check: ${out.ok.length} ok, ${out.drift.length} drift, ${out.notAssessed.length} not assessed`);
  if (out.drift.length) process.exit(1);
  if (out.notAssessed.length) process.exit(3);
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.checkMarketplace) return checkMarketplace(args);
  const ROOT = path.resolve(args.engine);
  const SKILLS_DIR = path.join(ROOT, args.root);
  const MANIFEST_PATH = path.join(ROOT, '.claude-plugin', 'plugin.json');
  const EXCLUDE_DIRS = new Set(args.exclude.split(',').map((s) => s.trim()).filter(Boolean));
  let pluginName = path.basename(ROOT);
  const marketplacePath = path.join(ROOT, '.claude-plugin', 'marketplace.json');
  if (fs.existsSync(marketplacePath)) {
    try {
      const marketplace = JSON.parse(fs.readFileSync(marketplacePath, 'utf8'));
      const rootPlugin = Array.isArray(marketplace.plugins) ? marketplace.plugins.find((p) => p.source === './' || p.source === '.') : null;
      if (rootPlugin && rootPlugin.name) pluginName = rootPlugin.name;
    } catch (e) { /* retain the directory fallback */ }
  }

  if (!fs.existsSync(SKILLS_DIR)) {
    console.error(`No skill root at ${SKILLS_DIR}`);
    process.exit(1);
  }

  const skillDirs = findSkillDirs(SKILLS_DIR, EXCLUDE_DIRS, []).sort();
  if (skillDirs.length === 0) {
    console.error(`No SKILL.md files found under ${SKILLS_DIR} — refusing to write an empty manifest.`);
    process.exit(1);
  }

  const skillPaths = skillDirs.map((p) => {
    const rel = path.relative(ROOT, p).split(path.sep).join('/');
    return './' + rel + '/';
  });

  const leafNames = new Map();
  let collision = false;
  for (const p of skillDirs) {
    const leaf = path.basename(p);
    if (leafNames.has(leaf)) {
      console.error(`Skill name collision: "${leaf}" at\n  ${leafNames.get(leaf)}\n  and\n  ${p}`);
      collision = true;
    }
    leafNames.set(leaf, p);
  }
  if (collision) process.exit(1);

  let existingManifest = {};
  if (fs.existsSync(MANIFEST_PATH)) {
    try {
      const parsed = JSON.parse(fs.readFileSync(MANIFEST_PATH, 'utf8'));
      if (parsed && typeof parsed === 'object' && !Array.isArray(parsed)) existingManifest = parsed;
    } catch (e) {
      /* ignore malformed existing file, regenerate */
    }
  }

  if (!existingManifest.userConfig || typeof existingManifest.userConfig !== 'object' || Array.isArray(existingManifest.userConfig)) {
    delete existingManifest.userConfig;
  }

  const manifest = {
    ...existingManifest,
    name: pluginName,
    version: args.version || existingManifest.version || '1.0.0',
    skills: skillPaths,
    mcpServers: {},
  };

  // If this engine ships a hooks/hooks.json, expose the standard on/off +
  // profile toggle at install time (Claude Code's userConfig mechanism) so
  // a user can control hook enforcement without editing files. Does NOT
  // declare "hooks" itself here — that stays auto-loaded by convention per
  // PLUGIN_SCHEMA_NOTES.md.
  if (fs.existsSync(path.join(ROOT, 'hooks', 'hooks.json'))) {
    manifest.userConfig = {
      ...(existingManifest.userConfig || {}),
      hooks_enabled: {
        type: 'boolean',
        title: 'Enable Chwezi hooks',
        description: 'Run this engine\'s enforcement hooks. Disable hook enforcement while keeping skills and agents available.',
        default: true,
      },
    };
  } else if (manifest.userConfig) {
    const { hooks_enabled: _hooksEnabled, ...remainingConfig } = manifest.userConfig;
    if (Object.keys(remainingConfig).length) manifest.userConfig = remainingConfig;
    else delete manifest.userConfig;
  }

  const rendered = JSON.stringify(manifest, null, 2) + '\n';

  if (args.check) {
    const current = fs.existsSync(MANIFEST_PATH) ? fs.readFileSync(MANIFEST_PATH, 'utf8').replace(/\r\n?/g, '\n') : null;
    if (current !== rendered) {
      console.error(`${path.basename(ROOT)}: plugin.json is stale (${skillPaths.length} skills on disk).`);
      process.exit(1);
    }
    console.log(`${path.basename(ROOT)}: plugin.json is current — ${skillPaths.length} skills.`);
    return;
  }

  fs.mkdirSync(path.dirname(MANIFEST_PATH), { recursive: true });
  fs.writeFileSync(MANIFEST_PATH, rendered);
  console.log(`${path.basename(ROOT)}: wrote plugin.json — ${skillPaths.length} skills.`);
}

main();
