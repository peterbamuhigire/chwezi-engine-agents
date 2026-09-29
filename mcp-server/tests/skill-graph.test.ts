import {mkdtemp, readdir, readFile, stat, writeFile} from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import {afterEach, describe, expect, it} from "vitest";
import {querySkillGraph} from "../src/skill-graph.js";

const saved = process.env["SKILLS_ENGINE_SKILL_GRAPH"];
afterEach(() => { if (saved === undefined) delete process.env["SKILLS_ENGINE_SKILL_GRAPH"]; else process.env["SKILLS_ENGINE_SKILL_GRAPH"] = saved; });

// Synthetic graph in the committed compact shape (nodes, edge_types, [from, to, type] edges).
const graph = {
  schema_version: "1.0",
  edge_types: ["links_to", "mentions", "routes_to", "similar_trigger"],
  provenance: {links_to: "EXTRACTED", mentions: "INFERRED", routes_to: "EXTRACTED", similar_trigger: "AMBIGUOUS"},
  nodes: ["router:engine-a", "skill:engine-a/skills/core/invoice-layout", "skill:engine-a/skills/core/ledger-posting", "skill:engine-b/skills/docs/printable-invoices"],
  edges: [[0, 1, 2], [0, 2, 2], [1, 2, 1], [3, 1, 0], [1, 3, 3]],
};

async function fixture(): Promise<string> {
  const root = await mkdtemp(path.join(os.tmpdir(), "skill-graph-"));
  const file = path.join(root, "skill-graph.json");
  await writeFile(file, JSON.stringify(graph));
  process.env["SKILLS_ENGINE_SKILL_GRAPH"] = file;
  return root;
}

async function snapshot(root: string): Promise<string[]> {
  const names = (await readdir(root)).sort();
  return Promise.all(names.map(async (name) => { const full = path.join(root, name); const info = await stat(full); return `${name} ${info.size} ${info.mtimeMs} ${(await readFile(full, "utf8")).length}`; }));
}

describe("query_skill_graph (read-only)", () => {
  it("returns neighbours for a known skill by unique suffix", async () => {
    await fixture();
    const result = await querySkillGraph("neighbours", "invoice-layout", undefined) as {node: string; outbound: {to: string; type: string}[]; inbound: {from: string}[]};
    expect(result.node).toBe("skill:engine-a/skills/core/invoice-layout");
    expect(result.outbound.map((e) => e.type).sort()).toEqual(["mentions", "similar_trigger"]);
    expect(result.inbound.map((e) => e.from).sort()).toEqual(["router:engine-a", "skill:engine-b/skills/docs/printable-invoices"]);
  });

  it("returns a path between two known skills and explains their edges", async () => {
    await fixture();
    const route = await querySkillGraph("path", "engine-b/skills/docs/printable-invoices", "ledger-posting") as {found: boolean; path: {from: string; to: string; type: string}[]};
    expect(route.found).toBe(true);
    expect(route.path.map((e) => e.type)).toEqual(["links_to", "mentions"]);
    const why = await querySkillGraph("explain", "invoice-layout", "printable-invoices") as {edges: {type: string; provenance: string}[]};
    expect(why.edges.map((e) => `${e.type}:${e.provenance}`).sort()).toEqual(["links_to:EXTRACTED", "similar_trigger:AMBIGUOUS"]);
  });

  it("rejects unknown operations and skills", async () => {
    await fixture();
    await expect(querySkillGraph("delete", "invoice-layout", undefined)).rejects.toMatchObject({code: "invalid_operation"});
    await expect(querySkillGraph("neighbours", "no-such-skill", undefined)).rejects.toMatchObject({code: "unknown_skill"});
  });

  it("writes nothing", async () => {
    const root = await fixture();
    const before = await snapshot(root);
    await querySkillGraph("neighbours", "invoice-layout", undefined);
    await querySkillGraph("path", "printable-invoices", "ledger-posting");
    expect(await snapshot(root)).toEqual(before);
  });
});
