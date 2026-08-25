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
    expect(identity.branch).toBe("main");
    expect(identity.id).toBe("uncatalogued");
    expect(identity.matched_catalog_entry).toBe(false);
  });
});
