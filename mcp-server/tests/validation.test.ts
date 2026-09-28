import {execFile} from "node:child_process";
import {mkdtemp, readFile, writeFile} from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import {fileURLToPath} from "node:url";
import {promisify} from "node:util";
import {afterEach, describe, expect, it} from "vitest";
import {parse} from "yaml";
import {validateEngine} from "../src/engine-validation.js";

const execFileAsync = promisify(execFile);
const repoRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..");
const liveCatalog = path.join(repoRoot, "catalog", "engines.yaml");
const originalCatalog = process.env["SKILLS_ENGINE_CATALOG"];
afterEach(() => { if (originalCatalog === undefined) delete process.env["SKILLS_ENGINE_CATALOG"]; else process.env["SKILLS_ENGINE_CATALOG"] = originalCatalog; });

async function fixtureEngine(validators: readonly string[]): Promise<{root: string; engine: string}> {
  const root = await mkdtemp(path.join(os.tmpdir(), "skills-engine-validation-"));
  const engine = path.join(root, "masking-fixture");
  await execFileAsync("git", ["init", "--quiet", engine], {windowsHide: true});
  const catalogFile = path.join(root, "engines.yaml");
  const items = validators.map((command) => `      - "${command}"`).join("\n");
  await writeFile(catalogFile, `schema_version: "1.0"\nengines:\n  - id: masking-fixture\n    repository: masking-fixture\n    path: masking-fixture\n    router: AGENTS.md\n    validators:\n${items}\n`);
  process.env["SKILLS_ENGINE_CATALOG"] = catalogFile;
  return {root, engine};
}

describe("declared validator execution", () => {
  it("does not let a passing validator mask an earlier failing one", async () => {
    const {root, engine} = await fixtureEngine(["exit 3", "exit 0"]);
    const result = await validateEngine(engine, "all", root);
    expect(result.checks.map((check) => check.status)).toEqual(["FAIL", "PASS"]);
    expect(result.checks[0]?.exit_code).toBe(3);
    expect(result.overall).toBe("FAIL");
  }, 60_000);

  it("reports PASS only when every listed validator passes", async () => {
    const {root, engine} = await fixtureEngine(["exit 0", "exit 0"]);
    const result = await validateEngine(engine, "all", root);
    expect(result.overall).toBe("PASS");
  }, 60_000);

  it("keeps every live catalogue validator as a separate, unpiped command", async () => {
    const catalog = parse(await readFile(liveCatalog, "utf8")) as {engines: {id: string; validators: string | string[]}[]};
    for (const entry of catalog.engines) {
      expect(Array.isArray(entry.validators), `${entry.id} validators must be a list`).toBe(true);
      for (const command of entry.validators as string[]) expect(command, `${entry.id}: ${command}`).not.toMatch(/\|/);
    }
  });
});
