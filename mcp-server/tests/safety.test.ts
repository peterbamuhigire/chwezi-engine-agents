import {mkdtemp, mkdir, writeFile} from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import {afterEach, describe, expect, it} from "vitest";
import {assertDeclaredValidator, assertSafeScope, requireConfirmationToken, resolveSafeTarget} from "../src/safety.js";

const originalToken = process.env["SKILLS_ENGINE_CONFIRMATION_TOKEN"];
afterEach(() => { if (originalToken === undefined) delete process.env["SKILLS_ENGINE_CONFIRMATION_TOKEN"]; else process.env["SKILLS_ENGINE_CONFIRMATION_TOKEN"] = originalToken; });

describe("MCP safety boundaries", () => {
  it("rejects a target outside the approved root", async () => {
    const parent = await mkdtemp(path.join(os.tmpdir(), "skills-engine-safety-"));
    const root = path.join(parent, "root");
    const outside = path.join(parent, "outside");
    await mkdir(root);
    await mkdir(outside);
    await writeFile(path.join(outside, "router.md"), "router");
    await expect(resolveSafeTarget(outside, root)).rejects.toMatchObject({code: "path_boundary"});
  });

  it("requires the host token and rejects model command text", () => {
    process.env["SKILLS_ENGINE_CONFIRMATION_TOKEN"] = "host-token-123";
    expect(() => requireConfirmationToken("wrong-token")).toThrowError(/confirmation token/);
    expect(() => assertDeclaredValidator("Remove-Item -Recurse", ["python scripts/check.py"])).toThrowError(/not declared/);
    expect(() => assertSafeScope("all; Remove-Item")).toThrowError(/contract identifier/);
  });
});
