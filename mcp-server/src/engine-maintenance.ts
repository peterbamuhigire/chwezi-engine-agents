import { execFile } from "node:child_process";
import { promisify } from "node:util";
import { discoverEngine, gitOutput } from "./engine-discovery.js";
import { ToolError } from "./contracts.js";
import type { MaintenanceResult } from "./contracts.js";
import { requireConfirmationToken } from "./safety.js";

const execFileAsync = promisify(execFile);
type Status = { readonly branch: string; readonly head: string; readonly dirty: boolean; readonly ahead: number; readonly behind: number };

async function status(root: string): Promise<Status> {
  const [branch, head, porcelain] = await Promise.all([gitOutput(root, ["branch", "--show-current"]), gitOutput(root, ["rev-parse", "HEAD"]), gitOutput(root, ["status", "--porcelain"]) ]);
  let ahead = 0;
  let behind = 0;
  try {
    const counts = await gitOutput(root, ["rev-list", "--left-right", "--count", "HEAD...@{u}"]);
    const parts = counts.split(/\s+/).map(Number);
    ahead = parts[0] ?? 0;
    behind = parts[1] ?? 0;
  } catch {
    throw new ToolError("upstream_unavailable", "The checkout has no readable upstream.", "Configure an upstream branch before requesting a pull.");
  }
  return {branch, head, dirty: porcelain.length > 0, ahead, behind};
}

function result(engineId: string, value: Status, pullResult: MaintenanceResult["pull_result"], blocker: string | null, beforeHead = value.head): MaintenanceResult {
  return {schema_version: "1.0", engine_id: engineId, before_head: beforeHead, after_head: value.head, branch: value.branch, working_tree: value.dirty ? "dirty" : "clean", pull_result: pullResult, ahead: value.ahead, behind: value.behind, blocker};
}

export async function inspectEngine(inputPath: string, approvedRoot = process.cwd()): Promise<MaintenanceResult> {
  const identity = await discoverEngine(inputPath, approvedRoot);
  const current = await status(identity.repo_root);
  return result(identity.id, current, "not_requested", null);
}

export async function pullEngineFastForward(inputPath: string, token: string, approvedRoot = process.cwd()): Promise<MaintenanceResult> {
  requireConfirmationToken(token);
  const identity = await discoverEngine(inputPath, approvedRoot);
  const before = await status(identity.repo_root);
  if (before.branch !== "main") throw new ToolError("branch_not_allowed", "Mutation target is not main.", "Change the requested scope explicitly before mutating a non-main branch.");
  if (before.dirty) return result(identity.id, before, "skipped_dirty", "Working tree is dirty; no pull was attempted.");
  if (before.ahead > 0) return result(identity.id, before, "blocked_diverged", "Local branch is ahead of its upstream; no pull was attempted.");
  try { await execFileAsync("git", ["-C", identity.repo_root, "pull", "--ff-only"], {timeout: 120_000, windowsHide: true}); }
  catch { const failed = await status(identity.repo_root).catch(() => before); return result(identity.id, failed, "failed", "git pull --ff-only failed; inspect the remote and checkout.", before.head); }
  const after = await status(identity.repo_root);
  return result(identity.id, after, after.head === before.head ? "already_current" : "updated", null, before.head);
}
