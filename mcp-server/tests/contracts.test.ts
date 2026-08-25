import {describe, expect, it} from "vitest";
import type {EngineIdentity, MaintenanceResult, ValidationResult} from "../src/contracts.js";

describe("shared MCP contracts", () => {
  it("keeps stable identity fields", () => {
    const identity: EngineIdentity = {id: "srs-skills", repository: "srs-skills", path: ".", repo_root: ".", remote: "", branch: "main", router: "AGENTS.md", matched_catalog_entry: true};
    expect(Object.keys(identity)).toEqual(["id", "repository", "path", "repo_root", "remote", "branch", "router", "matched_catalog_entry"]);
  });

  it("keeps verdict and maintenance enums typed", () => {
    const maintenance: MaintenanceResult = {schema_version: "1.0", engine_id: "srs-skills", before_head: "abc", after_head: "abc", branch: "main", working_tree: "clean", pull_result: "not_requested", ahead: 0, behind: 0, blocker: null};
    const validation: ValidationResult = {schema_version: "1.0", engine_id: "srs-skills", checks: [], overall: "NOT ASSESSED", next_action: "Inspect the dependency."};
    expect(maintenance.pull_result).toBe("not_requested");
    expect(validation.overall).toBe("NOT ASSESSED");
  });
});
