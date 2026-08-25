import { execFile } from "node:child_process";
import { promisify } from "node:util";
import { discoverEngine, catalogEntryFor } from "./engine-discovery.js";
import type { ValidationCheck, ValidationResult } from "./contracts.js";
import { assertDeclaredValidator, assertSafeScope, resolveSafeTarget } from "./safety.js";

const execFileAsync = promisify(execFile);

function commands(value: string | readonly string[]): readonly string[] { return typeof value === "string" ? [value] : value; }

async function runDeclared(command: string, cwd: string): Promise<ValidationCheck> {
  const started = Date.now();
  const executable = process.platform === "win32" ? "powershell.exe" : "/bin/sh";
  const args = process.platform === "win32" ? ["-NoProfile", "-NonInteractive", "-Command", command] : ["-c", command];
  try {
    const output = await execFileAsync(executable, args, {cwd, timeout: 120_000, windowsHide: true, maxBuffer: 1_000_000});
    const evidence = `${output.stdout.trim()}${output.stderr.trim()}`.trim() || "Command completed successfully.";
    return {command, status: "PASS", exit_code: 0, evidence, duration_ms: Date.now() - started};
  } catch (error: unknown) {
    const result = error as {code?: number | string; stdout?: string; stderr?: string};
    const exitCode = typeof result.code === "number" ? result.code : null;
    return {command, status: exitCode === null ? "NOT ASSESSED" : "FAIL", exit_code: exitCode, evidence: `${result.stdout ?? ""}${result.stderr ?? ""}`.trim() || "No command output.", duration_ms: Date.now() - started, ...(exitCode === null ? {reason: "Validator process or dependency was unavailable."} : {})};
  }
}

export async function validateEngine(inputPath: string, scope: string, approvedRoot = process.cwd()): Promise<ValidationResult> {
  assertSafeScope(scope);
  const target = await resolveSafeTarget(inputPath, approvedRoot);
  const identity = await discoverEngine(target, approvedRoot);
  const entry = await catalogEntryFor(identity);
  if (!entry) return {schema_version: "1.0", engine_id: identity.id, checks: [{command: "catalog lookup", status: "NOT ASSESSED", exit_code: null, evidence: "The repository is not catalogued.", duration_ms: null, reason: "No engine manifest or catalog entry was found."}], overall: "NOT ASSESSED", next_action: "Inspect the local router; do not invent a validator."};
  const declared = commands(entry.validators);
  const checks: ValidationCheck[] = [];
  for (const command of declared) {
    assertDeclaredValidator(command, declared);
    checks.push(await runDeclared(command, target));
  }
  const overall = checks.some((check) => check.status === "FAIL") ? "FAIL" : checks.some((check) => check.status === "NOT ASSESSED") ? "PARTIAL" : "PASS";
  return {schema_version: "1.0", engine_id: identity.id, checks, overall, next_action: overall === "PASS" ? "Review evidence and continue." : "Resolve failed or unassessed checks before release."};
}
