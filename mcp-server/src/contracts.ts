export type WorkingTree = "clean" | "dirty" | "missing";
export type PullResult = "not_requested" | "updated" | "already_current" | "skipped_dirty" | "blocked_diverged" | "failed";
export type Verdict = "PASS" | "FAIL" | "NOT ASSESSED";

export interface EngineIdentity {
  readonly id: string;
  readonly repository: string;
  readonly path: string;
  readonly repo_root: string;
  readonly remote: string;
  readonly branch: string;
  readonly router: string | null;
  readonly matched_catalog_entry: boolean;
}

export interface MaintenanceResult {
  readonly schema_version: "1.0";
  readonly engine_id: string;
  readonly before_head: string | null;
  readonly after_head: string | null;
  readonly branch: string;
  readonly working_tree: WorkingTree;
  readonly pull_result: PullResult;
  readonly ahead: number;
  readonly behind: number;
  readonly blocker: string | null;
}

export interface ValidationCheck {
  readonly command: string;
  readonly status: Verdict;
  readonly exit_code: number | null;
  readonly evidence: string;
  readonly duration_ms: number | null;
  readonly reason?: string;
}

export interface ValidationResult {
  readonly schema_version: "1.0";
  readonly engine_id: string;
  readonly checks: readonly ValidationCheck[];
  readonly overall: "PASS" | "FAIL" | "PARTIAL" | "NOT ASSESSED";
  readonly next_action: string;
}

export class ToolError extends Error {
  public readonly code: string;
  public readonly remediation: string;

  public constructor(code: string, message: string, remediation: string) {
    super(message);
    this.name = "ToolError";
    this.code = code;
    this.remediation = remediation;
  }
}
