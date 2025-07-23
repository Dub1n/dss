import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
// Create a simple server
const server = new McpServer({
    name: "dss-guardrails",
    version: "1.0.0"
});
// Register a simple test tool with a different name
server.tool("dss_guardrails", async () => {
    console.error("[alternate] dss_guardrails tool called");
    return {
        content: [{ type: "text", text: "DSS Guardrails rules applied!" }]
    };
});
// Register another tool with a simple name
server.tool("guardrails", async () => {
    console.error("[alternate] guardrails tool called");
    return {
        content: [{ type: "text", text: "Guardrails activated!" }]
    };
});
// Start the server
console.error("[alternate] Starting server...");
const transport = new StdioServerTransport();
await server.connect(transport);
console.error("[alternate] Server connected successfully");
// Keep the process running
process.on('SIGINT', () => {
    console.error("[alternate] Shutting down...");
    process.exit(0);
});
