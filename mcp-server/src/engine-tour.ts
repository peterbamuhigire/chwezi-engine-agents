import { readFile, realpath, stat } from "node:fs/promises";
import path from "node:path";
import { parse } from "yaml";
import { ToolError } from "./contracts.js";
import { resolveSafeTarget } from "./safety.js";

// Read-only engine tour lookup (M10-12-T07, UA-10). It resolves the engine through the approved
// root, returns the committed docs/engine-tours/<id>.json and marks it stale when the engine HEAD
// differs from generated_from_commit. It never runs a process (Python or Git) and never writes:
// HEAD is read from the .git directory as data.

const COORDINATION = "chwezi-engine-agents";
type CatalogEntry = { readonly id: string; readonly repository?: string; readonly path?: string };

export interface EngineTourResult {
  readonly engine_id: string;
  readonly repo_root: string;
  readonly head: string | null;
  readonly generated_from_commit: string | null;
  readonly stale: boolean | null;
  readonly tour: unknown;
}

function catalogPath(): string { return process.env["SKILLS_ENGINE_CATALOG"] ?? path.resolve(process.cwd(), "catalog", "engines.yaml"); }
function toursDir(): string { return process.env["SKILLS_ENGINE_TOURS_DIR"] ?? path.resolve(process.cwd(), "docs", "engine-tours"); }

async function exists(target: string): Promise<boolean> {
  try { await stat(target); return true; } catch { return false; }
}

async function repositoryRoot(target: string, approvedRoot: string): Promise<string> {
  const boundary = await realpath(approvedRoot);
  let current = target;
  for (;;) {
    if (await exists(path.join(current, ".git"))) return current;
    const parent = path.dirname(current);
    const relative = path.relative(boundary, parent);
    if (parent === current || relative.startsWith("..") || path.isAbsolute(relative)) break;
    current = parent;
  }
  throw new ToolError("engine_unresolved", "No engine checkout contains the target inside the approved root.", "Pass a path inside an engine checkout.");
}

async function readHead(repoRoot: string): Promise<string | null> {
  try {
    let gitDir = path.join(repoRoot, ".git");
    const info = await stat(gitDir);
    if (info.isFile()) {
      const pointer = (await readFile(gitDir, "utf8")).trim();
      if (!pointer.startsWith("gitdir:")) return null;
      gitDir = path.resolve(repoRoot, pointer.slice("gitdir:".length).trim());
    }
    const head = (await readFile(path.join(gitDir, "HEAD"), "utf8")).trim();
    if (!head.startsWith("ref:")) return /^[0-9a-f]{40}$/.test(head) ? head : null;
    const refName = head.slice(4).trim();
    if (!/^refs\/[A-Za-z0-9._\/-]+$/.test(refName)) return null;
    try {
      const value = (await readFile(path.join(gitDir, ...refName.split("/")), "utf8")).trim();
      if (/^[0-9a-f]{40}$/.test(value)) return value;
    } catch { /* fall through to packed-refs */ }
    const commonDir = await readFile(path.join(gitDir, "commondir"), "utf8").then((v) => path.resolve(gitDir, v.trim())).catch(() => gitDir);
    const packed = await readFile(path.join(commonDir, "packed-refs"), "utf8").catch(() => "");
    for (const line of packed.split(/\r?\n/)) {
      const [sha, name] = line.split(" ");
      if (name === refName && sha && /^[0-9a-f]{40}$/.test(sha)) return sha;
    }
    const loose = await readFile(path.join(commonDir, ...refName.split("/")), "utf8").catch(() => "");
    return /^[0-9a-f]{40}$/.test(loose.trim()) ? loose.trim() : null;
  } catch {
    return null;
  }
}

async function engineIdFor(folder: string): Promise<string> {
  if (folder === COORDINATION) return COORDINATION;
  let entries: CatalogEntry[] = [];
  try {
    const value = parse(await readFile(catalogPath(), "utf8")) as { engines?: CatalogEntry[] };
    entries = value.engines ?? [];
  } catch {
    throw new ToolError("catalog_unavailable", "The engine catalog could not be read.", "Set SKILLS_ENGINE_CATALOG to a readable catalog/engines.yaml.");
  }
  const entry = entries.find((candidate) => candidate.path === folder || candidate.repository === folder);
  if (!entry) throw new ToolError("engine_uncatalogued", "The checkout is not a catalogued engine.", "Use a catalogued engine or chwezi-engine-agents.");
  return entry.id;
}

export async function engineTour(inputPath: string, approvedRoot = process.cwd()): Promise<EngineTourResult> {
  const target = await resolveSafeTarget(inputPath, approvedRoot);
  const repoRoot = await repositoryRoot(target, approvedRoot);
  const engineId = await engineIdFor(path.basename(repoRoot));
  if (!/^[a-z0-9][a-z0-9-]{0,63}$/.test(engineId)) throw new ToolError("invalid_engine_id", "Engine id is not a safe file name.", "Correct the catalog entry.");
  let tour: {generated_from_commit?: unknown};
  try {
    tour = JSON.parse(await readFile(path.join(toursDir(), `${engineId}.json`), "utf8")) as {generated_from_commit?: unknown};
  } catch {
    throw new ToolError("tour_unavailable", "No committed tour exists for this engine.", "Run scripts/generate_engine_tour.py in chwezi-engine-agents and commit docs/engine-tours.");
  }
  const generated = typeof tour.generated_from_commit === "string" ? tour.generated_from_commit : null;
  const head = await readHead(repoRoot);
  const stale = head === null || generated === null ? null : head !== generated;
  return {engine_id: engineId, repo_root: repoRoot, head, generated_from_commit: generated, stale, tour};
}
