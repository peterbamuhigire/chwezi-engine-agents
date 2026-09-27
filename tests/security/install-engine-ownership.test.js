'use strict';

const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { spawnSync } = require('node:child_process');

const REPO = path.resolve(__dirname, '..', '..');
const INSTALLER = path.join(REPO, 'scripts', 'install-engine.js');
const SANDBOX = fs.mkdtempSync(path.join(os.tmpdir(), 'chwezi-installer-security-'));

function write(file, contents) {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, contents, 'utf8');
}

function run(cwd, ...args) {
  return spawnSync(process.execPath, [INSTALLER, ...args], {
    cwd,
    encoding: 'utf8',
    windowsHide: true,
  });
}

function makeEngine(root, content = 'engine version 1\n') {
  write(path.join(root, '.claude-plugin', 'plugin.json'), JSON.stringify({
    version: '1.0.0', skills: ['./skills/demo/'],
  }));
  write(path.join(root, 'skills', 'demo', 'SKILL.md'), content);
}

function assertRefused(result, pattern, message) {
  assert.notEqual(result.status, 0, message);
  assert.match(result.stderr, pattern, message);
}

function removeSandboxed(target) {
  const relative = path.relative(SANDBOX, path.resolve(target));
  assert.notEqual(relative, '..');
  assert.equal(relative.startsWith('..' + path.sep), false);
  assert.equal(path.isAbsolute(relative), false);
  fs.rmSync(target, { recursive: true, force: true });
}

try {
  const workspace = path.join(SANDBOX, 'workspace');
  const engine = path.join(SANDBOX, 'engine');
  const target = path.join(workspace, '.claude');
  const statePath = path.join(target, '.chwezi', 'install-state.json');
  makeEngine(engine);

  // First install must not replace an unrelated pre-existing user file.
  const collision = path.join(target, 'skills', 'demo', 'SKILL.md');
  write(collision, 'user-owned content\n');
  const firstInstall = run(workspace, 'install', '--engine', engine, '--scope', 'project');
  assertRefused(firstInstall, /unowned destination/i, 'first install should reject an unowned collision');
  assert.equal(fs.readFileSync(collision, 'utf8'), 'user-owned content\n');

  removeSandboxed(target);
  fs.mkdirSync(collision, { recursive: true });
  const typeCollision = run(workspace, 'install', '--engine', engine, '--scope', 'project', '--force');
  assertRefused(typeCollision, /file\/directory or special-file collision/i, 'force must not replace a directory with a managed file');
  removeSandboxed(target);
  let result = run(workspace, 'install', '--engine', engine, '--scope', 'project');
  assert.equal(result.status, 0, result.stderr);
  const installed = path.join(target, 'skills', 'demo', 'SKILL.md');
  write(path.join(target, 'user-notes.txt'), 'keep this unrelated file\n');

  // Updates preserve a user's local edit unless the explicit force flag is used.
  write(installed, 'user local edit\n');
  makeEngine(engine, 'engine version 2\n');
  result = run(workspace, 'install', '--engine', engine, '--scope', 'project');
  assertRefused(result, /locally modified installed file/i, 'update should reject a locally modified owned file');
  assert.equal(fs.readFileSync(installed, 'utf8'), 'user local edit\n');

  // A normal update is allowed after the user restores the installed bytes.
  write(installed, 'engine version 1\n');
  write(path.join(engine, 'skills', 'demo', 'NEW.md'), 'new source file\n');
  result = run(workspace, 'install', '--engine', engine, '--scope', 'project');
  assert.equal(result.status, 0, result.stderr);
  assert.equal(fs.readFileSync(installed, 'utf8'), 'engine version 2\n');
  assert.equal(fs.readFileSync(path.join(target, 'skills', 'demo', 'NEW.md'), 'utf8'), 'new source file\n');
  assert.equal(fs.readFileSync(path.join(target, 'user-notes.txt'), 'utf8'), 'keep this unrelated file\n');

  // Uninstall refuses local edits and leaves unrelated files untouched.
  write(installed, 'user local edit after update\n');
  result = run(workspace, 'uninstall', '--engine', path.basename(engine), '--scope', 'project');
  assertRefused(result, /modified since install/i, 'uninstall should reject a locally modified owned file');
  assert.equal(fs.readFileSync(installed, 'utf8'), 'user local edit after update\n');
  assert.equal(fs.readFileSync(path.join(target, 'user-notes.txt'), 'utf8'), 'keep this unrelated file\n');
  write(installed, 'engine version 2\n');
  result = run(workspace, 'uninstall', '--engine', path.basename(engine), '--scope', 'project');
  assert.equal(result.status, 0, result.stderr);
  assert.equal(fs.existsSync(path.join(target, 'skills', 'demo')), false);
  assert.equal(fs.readFileSync(path.join(target, 'user-notes.txt'), 'utf8'), 'keep this unrelated file\n');

  // A tampered state record cannot make uninstall escape the managed root.
  const externalSentinel = path.join(SANDBOX, 'outside.txt');
  write(externalSentinel, 'keep outside target\n');
  write(statePath, JSON.stringify({ version: 1, engines: {
    hostile: { files: { '../../outside.txt': '0'.repeat(64) } },
  } }));
  result = run(workspace, 'uninstall', '--engine', 'hostile', '--scope', 'project');
  assertRefused(result, /escapes its allowed root/i, 'uninstall should reject a traversing ownership record');
  assert.equal(fs.readFileSync(externalSentinel, 'utf8'), 'keep outside target\n');

  // Manifest paths cannot escape either source or destination roots.
  const hostileEngine = path.join(SANDBOX, 'hostile-engine');
  write(path.join(hostileEngine, '.claude-plugin', 'plugin.json'), JSON.stringify({
    version: '1.0.0', skills: ['./skills/../../outside/'],
  }));
  write(path.join(SANDBOX, 'outside', 'SKILL.md'), 'must not be copied\n');
  result = run(workspace, 'install', '--engine', hostileEngine, '--scope', 'project');
  assertRefused(result, /escapes its allowed root/i, 'manifest traversal should be refused');
  assert.equal(fs.existsSync(path.join(workspace, 'outside', 'SKILL.md')), false);

  // Corrupt ownership state fails closed rather than being treated as empty.
  write(statePath, '{not valid json');
  const safeCollision = path.join(target, 'skills', 'demo', 'SKILL.md');
  write(safeCollision, 'preserve me\n');
  result = run(workspace, 'install', '--engine', engine, '--scope', 'project');
  assertRefused(result, /unsafe or unreadable installer state/i, 'invalid state should fail closed');
  assert.equal(fs.readFileSync(safeCollision, 'utf8'), 'preserve me\n');

  console.log('install-engine ownership security: PASS (unowned collision, modified update/uninstall, update preservation, path traversal and corrupt state)');
} finally {
  const tempRoot = path.resolve(os.tmpdir());
  assert.notEqual(path.relative(tempRoot, SANDBOX), '..');
  assert.equal(path.relative(tempRoot, SANDBOX).startsWith('..' + path.sep), false);
  fs.rmSync(SANDBOX, { recursive: true, force: true });
}
