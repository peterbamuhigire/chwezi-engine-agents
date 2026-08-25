import { constants } from "node:fs";
import { access, realpath } from "node:fs/promises";
import path from "node:path";
import { timingSafeEqual } from "node:crypto";
import { ToolError } from "./contracts.js";

function isWithin(root: string, target: string): boolean {
  const relative = path.relative(root, target);
  return relative === "" || (!relative.startsWith(`..${path.sep}`) && relative !== ".." && !path.isAbsolute(relative));
}

export async function resolveSafeTarget(inputPath: string, approvedRoot: string): Promise<string> {
  if (inputPath.trim() === "") throw new ToolError("invalid_path", "Target path is empty.", "Provide an existing engine checkout path.");
  let root: string;
  let target: string;
  try {
    [root, target] = await Promise.all([realpath(approvedRoot), realpath(inputPath)]);
  } catch {
    throw new ToolError("path_unavailable", "Target or approved root does not exist.", "Use an existing checkout beneath the configured workspace root.");
  }
  if (!isWithin(root, target)) throw new ToolError("path_boundary", "Target resolves outside the approved workspace root.", "Choose a path inside the configured workspace root.");
  await access(target, constants.R_OK);
  return target;
}

export function assertSafeScope(scope: string): void {
  if (!/^[A-Za-z0-9_-]+$/.test(scope) || scope.length > 64) throw new ToolError("invalid_scope", "Scope is not a contract identifier.", "Use a simple declared scope such as all or structural.");
}

export function requireConfirmationToken(token: string): void {
  const expected = process.env["SKILLS_ENGINE_CONFIRMATION_TOKEN"];
  if (!expected || !token || expected.length !== token.length || !timingSafeEqual(Buffer.from(expected), Buffer.from(token))) throw new ToolError("approval_required", "A valid host confirmation token is required.", "Ask the host to issue a confirmation token for this exact mutation.");
}

export function assertDeclaredValidator(command: string, declaredCommands: readonly string[]): void {
  if (!declaredCommands.includes(command)) throw new ToolError("validator_not_allowlisted", "The validator is not declared by the engine catalog.", "Use a validator declared in catalog/engines.yaml or the engine manifest.");
}
