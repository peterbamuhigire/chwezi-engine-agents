import {copyFile, mkdir, mkdtemp, readFile, readdir, stat, writeFile} from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import {fileURLToPath} from "node:url";
import {afterEach, beforeEach, describe, expect, it} from "vitest";
import {engineTour} from "../src/engine-tour.js";

const repoRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..");
const committedTours = path.join(repoRoot, "docs", "engine-tours");
const saved = {catalog: process.env["SKILLS_ENGINE_CATALOG"], tours: process.env["SKILLS_ENGINE_TOURS_DIR"]};

function restore(name: string, value: string | undefined): void { if (value === undefined) delete process.env[name]; else process.env[name] = value; }

async function snapshot(root: string): Promise<string[]> {
  const entries: string[] = [];
  async function walk(folder: string): Promise<void> {
    for (const entry of (await readdir(folder, {withFileTypes: true})).sort((a, b) => a.name.localeCompare(b.name))) {
      const full = path.join(folder, entry.name);
      if (entry.isDirectory()) { entries.push(`d ${path.relative(root, full)}`); await walk(full); }
      else { const info = await stat(full); entries.push(`f ${path.relative(root, full)} ${info.size} ${info.mtimeMs} ${(await readFile(full)).toString("base64")}`); }
    }
  }
  await walk(root);
  return entries;
}

// A synthetic workspace: a dev-engine folder whose .git holds HEAD as data (no Git process), the
// live catalogue, and the committed dev tour.
async function workspace(head: string): Promise<{root: string; engine: string}> {
  const root = await mkdtemp(path.join(os.tmpdir(), "engine-tour-"));
  const engine = path.join(root, "chwezi-dev-engine");
  await mkdir(path.join(engine, ".git", "refs", "heads"), {recursive: true});
  await mkdir(path.join(engine, "skills"), {recursive: true});
  await writeFile(path.join(engine, ".git", "HEAD"), "ref: refs/heads/main\n");
  await writeFile(path.join(engine, ".git", "refs", "heads", "main"), `${head}\n`);
  const tours = path.join(root, "tours");
  await mkdir(tours);
  await copyFile(path.join(committedTours, "chwezi-dev-engine.json"), path.join(tours, "chwezi-dev-engine.json"));
  process.env["SKILLS_ENGINE_CATALOG"] = path.join(repoRoot, "catalog", "engines.yaml");
  process.env["SKILLS_ENGINE_TOURS_DIR"] = tours;
  return {root, engine};
}

async function committedCommit(): Promise<string> {
  const tour = JSON.parse(await readFile(path.join(committedTours, "chwezi-dev-engine.json"), "utf8")) as {generated_from_commit: string};
  return tour.generated_from_commit;
}

describe("engine_tour (read-only)", () => {
  beforeEach(() => { delete process.env["SKILLS_ENGINE_TOURS_DIR"]; });
  afterEach(() => { restore("SKILLS_ENGINE_CATALOG", saved.catalog); restore("SKILLS_ENGINE_TOURS_DIR", saved.tours); });

  it("returns the dev tour, fresh when HEAD matches the tour commit", async () => {
    const commit = await committedCommit();
    const {root, engine} = await workspace(commit);
    const result = await engineTour(path.join(engine, "skills"), root);
    expect(result.engine_id).toBe("chwezi-dev-engine");
    expect(result.stale).toBe(false);
    const tour = result.tour as {engine_id: string; steps: unknown[]};
    expect(tour.engine_id).toBe("chwezi-dev-engine");
    expect(tour.steps.length).toBeGreaterThanOrEqual(7);
  });

  it("reports stale: true when the engine HEAD has moved", async () => {
    const {root, engine} = await workspace("0".repeat(40));
    const result = await engineTour(engine, root);
    expect(result.stale).toBe(true);
    expect(result.head).toBe("0".repeat(40));
  });

  it("refuses a path outside the approved root with path_boundary", async () => {
    const {root} = await workspace(await committedCommit());
    const approved = path.join(root, "chwezi-dev-engine");
    await expect(engineTour(path.join(root, "tours"), approved)).rejects.toMatchObject({code: "path_boundary"});
  });

  it("writes nothing", async () => {
    const {root, engine} = await workspace(await committedCommit());
    const before = await snapshot(root);
    await engineTour(engine, root);
    await engineTour(path.join(engine, "skills"), root);
    await expect(engineTour(path.join(root, "tours"), path.join(root, "chwezi-dev-engine"))).rejects.toBeTruthy();
    expect(await snapshot(root)).toEqual(before);
  });
});
