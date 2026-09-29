import { readFile } from "node:fs/promises";
import path from "node:path";
import { ToolError } from "./contracts.js";

// Read-only query over the committed report-only skill graph (M10-12-T09, GR-03).
// docs/skill-graph/skill-graph.json is produced by scripts/skill_graph.py. The graph is never a
// routing input or a gate (P04); this tool only answers neighbours, path and explain questions.
// It never runs a process and never writes.

interface Graph {
  readonly edge_types: readonly string[];
  readonly provenance: Readonly<Record<string, string>>;
  readonly nodes: readonly string[];
  readonly edges: readonly (readonly [number, number, number])[];
  readonly generated_from_commits?: Readonly<Record<string, string>>;
}

export interface EdgeView { readonly from: string; readonly to: string; readonly type: string; readonly provenance: string }

const MAX_NEIGHBOURS = 200;
const MAX_DEPTH = 6;

function graphPath(): string { return process.env["SKILLS_ENGINE_SKILL_GRAPH"] ?? path.resolve(process.cwd(), "docs", "skill-graph", "skill-graph.json"); }

export async function loadGraph(): Promise<Graph> {
  try {
    const graph = JSON.parse(await readFile(graphPath(), "utf8")) as Graph;
    if (!Array.isArray(graph.nodes) || !Array.isArray(graph.edges) || !Array.isArray(graph.edge_types)) throw new Error("shape");
    return graph;
  } catch {
    throw new ToolError("graph_unavailable", "The committed skill graph could not be read.", "Run scripts/skill_graph.py --out docs/skill-graph in chwezi-engine-agents.");
  }
}

export function resolveNode(graph: Graph, query: string): number {
  const text = query.trim();
  if (text === "" || text.length > 300) throw new ToolError("invalid_input", "Skill identifier is empty or too long.", "Pass a node id such as skill:<engine>/<path> or a unique suffix.");
  const exact = graph.nodes.indexOf(text);
  if (exact >= 0) return exact;
  const withPrefix = graph.nodes.indexOf(`skill:${text}`);
  if (withPrefix >= 0) return withPrefix;
  const matches = graph.nodes.flatMap((node, index) => (node.startsWith("skill:") && (node.endsWith(`/${text}`) || node === `skill:${text}`) ? [index] : []));
  if (matches.length === 1 && matches[0] !== undefined) return matches[0];
  if (matches.length > 1) throw new ToolError("ambiguous_skill", `The identifier matches ${matches.length} skills.`, "Use the full node id, for example skill:<engine>/<path>.");
  throw new ToolError("unknown_skill", "No skill node matches the identifier.", "Check the node id against docs/skill-graph/skill-graph.json.");
}

function view(graph: Graph, edge: readonly [number, number, number]): EdgeView {
  const type = graph.edge_types[edge[2]] ?? "unknown";
  return {from: graph.nodes[edge[0]] ?? "?", to: graph.nodes[edge[1]] ?? "?", type, provenance: graph.provenance[type] ?? "UNKNOWN"};
}

export function neighbours(graph: Graph, query: string): {node: string; outbound: EdgeView[]; inbound: EdgeView[]; truncated: boolean} {
  const index = resolveNode(graph, query);
  const outbound = graph.edges.filter((e) => e[0] === index).map((e) => view(graph, e));
  const inbound = graph.edges.filter((e) => e[1] === index).map((e) => view(graph, e));
  const truncated = outbound.length > MAX_NEIGHBOURS || inbound.length > MAX_NEIGHBOURS;
  return {node: graph.nodes[index] ?? query, outbound: outbound.slice(0, MAX_NEIGHBOURS), inbound: inbound.slice(0, MAX_NEIGHBOURS), truncated};
}

export function shortestPath(graph: Graph, fromQuery: string, toQuery: string): {path: EdgeView[]; found: boolean} {
  const start = resolveNode(graph, fromQuery);
  const goal = resolveNode(graph, toQuery);
  const adjacency = new Map<number, (readonly [number, number, number])[]>();
  for (const edge of graph.edges) {
    const list = adjacency.get(edge[0]) ?? [];
    list.push(edge);
    adjacency.set(edge[0], list);
  }
  const previous = new Map<number, readonly [number, number, number]>();
  const seen = new Set<number>([start]);
  let frontier = [start];
  for (let depth = 0; depth < MAX_DEPTH && frontier.length > 0 && !seen.has(goal); depth += 1) {
    const next: number[] = [];
    for (const node of frontier) {
      for (const edge of adjacency.get(node) ?? []) {
        if (seen.has(edge[1])) continue;
        seen.add(edge[1]);
        previous.set(edge[1], edge);
        next.push(edge[1]);
      }
    }
    frontier = next;
  }
  if (!seen.has(goal) || start === goal) return {path: [], found: start === goal};
  const steps: EdgeView[] = [];
  let cursor = goal;
  while (cursor !== start) {
    const edge = previous.get(cursor);
    if (!edge) break;
    steps.unshift(view(graph, edge));
    cursor = edge[0];
  }
  return {path: steps, found: true};
}

export function explain(graph: Graph, fromQuery: string, toQuery: string): {edges: EdgeView[]} {
  const a = resolveNode(graph, fromQuery);
  const b = resolveNode(graph, toQuery);
  return {edges: graph.edges.filter((e) => (e[0] === a && e[1] === b) || (e[0] === b && e[1] === a)).map((e) => view(graph, e))};
}

export async function querySkillGraph(operation: string, skill: string, target: string | undefined): Promise<unknown> {
  const graph = await loadGraph();
  const note = "Report-only graph: never a routing input or a gate (P04). INFERRED and AMBIGUOUS edges are evidence to check, not facts.";
  switch (operation) {
    case "neighbours": return {note, ...neighbours(graph, skill)};
    case "path":
      if (target === undefined) throw new ToolError("invalid_input", "path needs a target.", "Pass target with the second skill.");
      return {note, ...shortestPath(graph, skill, target)};
    case "explain":
      if (target === undefined) throw new ToolError("invalid_input", "explain needs a target.", "Pass target with the second skill.");
      return {note, ...explain(graph, skill, target)};
    default: throw new ToolError("invalid_operation", "Operation must be neighbours, path or explain.", "Choose one of the three operations.");
  }
}
