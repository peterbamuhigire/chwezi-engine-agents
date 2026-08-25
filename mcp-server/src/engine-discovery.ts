import { execFile } from "node:child_process";
import { promisify } from "node:util";
import path from "node:path";
import { readFile } from "node:fs/promises";
import { parse } from "yaml";
import { ToolError } from "./contracts.js";
import type { EngineIdentity } from "./contracts.js";
import { resolveSafeTarget } from "./safety.js";

const execFileAsync = promisify(execFile);
type CatalogEntry = { readonly id: string; readonly repository: string; readonly path: string; readonly router: string; readonly validators: string | readonly string[] };

function catalogPath(): string { return process.env["SKILLS_ENGINE_CATALOG"] ?? path.resolve(process.cwd(), "catalog", "engines.yaml"); }

async function git(root: string, args: readonly string[]): Promise<string> {
  try {
    const result = await execFileAsync("git", ["-C", root, ...args], { timeout: 10_000, windowsHide: true });
    return result.stdout.trim();
  } catch {
    throw new ToolError("git_unavailable", "Git inspection failed for the target.", "Use a readable Git checkout with Git available on PATH.");
  }
}

async function catalog(): Promise<readonly CatalogEntry[]> {
  try {
    const raw = await readFile(catalogPath(), "utf8");
    const value = parse(raw) as { engines?: CatalogEntry[] };
    return value.engines ?? [];
  } catch {
    throw new ToolError("catalog_unavailable", "The engine catalog could not be read.", "Set SKILLS_ENGINE_CATALOG to a readable catalog/engines.yaml.");
  }
}

export async function discoverEngine(inputPath: string, approvedRoot = process.cwd()): Promise<EngineIdentity> {
  const target = await resolveSafeTarget(inputPath, approvedRoot);
  const repoRoot = await git(target, ["rev-parse", "--show-toplevel"]);
  const remote = await git(repoRoot, ["remote", "get-url", "origin"]).catch(() => "");
  const branch = await git(repoRoot, ["branch", "--show-current"]).catch(() => "");
  const folder = path.basename(repoRoot);
  const repository = remote.split("/").pop()?.replace(/\.git$/, "") ?? folder;
  const entries = await catalog();
  const entry = entries.find((candidate) => candidate.repository === repository || candidate.path === folder);
  let router: string | null = entry?.router ?? null;
  if (router === null) {
    try { await readFile(path.join(repoRoot, "AGENTS.md"), "utf8"); router = "AGENTS.md"; }
    catch { try { await readFile(path.join(repoRoot, "README.md"), "utf8"); router = "README.md"; } catch { router = null; } }
  }
  return {id: entry?.id ?? "uncatalogued", repository, path: inputPath, repo_root: repoRoot, remote, branch, router, matched_catalog_entry: entry !== undefined};
}

export async function catalogEntryFor(identity: EngineIdentity): Promise<CatalogEntry | undefined> {
  const entries = await catalog();
  return entries.find((candidate) => candidate.id === identity.id);
}

export async function gitOutput(root: string, args: readonly string[]): Promise<string> { return git(root, args); }
