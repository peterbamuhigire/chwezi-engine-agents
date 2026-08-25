import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { CallToolRequestSchema, ListToolsRequestSchema } from "@modelcontextprotocol/sdk/types.js";
import { discoverEngine } from "./engine-discovery.js";
import { inspectEngine, pullEngineFastForward } from "./engine-maintenance.js";
import { validateEngine } from "./engine-validation.js";
import { ToolError } from "./contracts.js";

const server = new Server({name: "skills-engine-agents-mcp", version: "1.0.0"}, {capabilities: {tools: {}}});
const approvedRoot = process.env["SKILLS_ENGINE_WORKSPACE_ROOT"] ?? process.cwd();
server.setRequestHandler(ListToolsRequestSchema, async () => ({tools: [
  {name: "discover_engine", description: "Read-only Git-root and catalog discovery.", inputSchema: {type: "object", properties: {path: {type: "string"}}, required: ["path"]}},
  {name: "inspect_engine", description: "Read-only engine Git status and upstream inspection.", inputSchema: {type: "object", properties: {path: {type: "string"}}, required: ["path"]}},
  {name: "validate_engine", description: "Run only validators declared by the catalog or engine manifest.", inputSchema: {type: "object", properties: {path: {type: "string"}, scope: {type: "string"}}, required: ["path", "scope"]}},
  {name: "pull_engine_ff_only", description: "Approval-gated fast-forward-only pull.", inputSchema: {type: "object", properties: {path: {type: "string"}, confirmation_token: {type: "string"}}, required: ["path", "confirmation_token"]}},
]}));

function textResult(value: unknown): {content: [{type: "text"; text: string}]} { return {content: [{type: "text", text: JSON.stringify(value, null, 2)}]}; }
function input(request: {params: {arguments?: Record<string, unknown> | undefined}}): Record<string, unknown> { return request.params.arguments ?? {}; }
function stringArg(args: Record<string, unknown>, name: string): string {
  const value = args[name];
  if (typeof value !== "string") throw new ToolError("invalid_input", `${name} must be a string.`, `Provide a string ${name}.`);
  return value;
}

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  try {
    const args = input(request);
    switch (request.params.name) {
      case "discover_engine": return textResult(await discoverEngine(stringArg(args, "path"), approvedRoot));
      case "inspect_engine": return textResult(await inspectEngine(stringArg(args, "path"), approvedRoot));
      case "validate_engine": return textResult(await validateEngine(stringArg(args, "path"), stringArg(args, "scope"), approvedRoot));
      case "pull_engine_ff_only": return textResult(await pullEngineFastForward(stringArg(args, "path"), stringArg(args, "confirmation_token"), approvedRoot));
      default: throw new ToolError("unknown_tool", "Tool is not registered.", "Use one of the four typed tools listed by the server.");
    }
  } catch (error: unknown) {
    const toolError = error instanceof ToolError ? error : new ToolError("tool_failure", "Tool execution failed.", "Inspect the server logs and retry with a valid contract.");
    return {isError: true, content: [{type: "text", text: JSON.stringify({code: toolError.code, message: toolError.message, remediation: toolError.remediation})}]};
  }
});

await server.connect(new StdioServerTransport());
