import {execFileSync} from "node:child_process";
import path from "node:path";
import {fileURLToPath} from "node:url";
import {describe, expect, it} from "vitest";
import {discoverEngine} from "../src/engine-discovery.js";

const repoRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..");
process.env["SKILLS_ENGINE_CATALOG"] = path.join(repoRoot, "catalog", "engines.yaml");

describe("engine discovery", () => {
  it("returns the stable identity contract for this checkout", async () => {
    const identity = await discoverEngine(repoRoot, repoRoot);
    expect(path.resolve(identity.repo_root.replaceAll("/", path.sep))).toBe(path.resolve(repoRoot));
    // The checkout's own branch: this test must pass on main, on a Kaizen branch and on a detached HEAD (empty).
    const branch = execFileSync("git", ["branch", "--show-current"], {cwd: repoRoot, encoding: "utf8", windowsHide: true}).trim();
    expect(identity.branch).toBe(branch);
    expect(identity.id).toBe("uncatalogued");
    expect(identity.matched_catalog_entry).toBe(false);
  });
});
