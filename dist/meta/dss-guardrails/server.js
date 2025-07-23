import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
// Enable debug logging
process.env.DEBUG = '*';
const RULES = `
Enforce the DSS 5-step assistant workflow exactly as written:
1  Understand & Gather Context
2  Identify the correct workflow (00-workflow-selection.mdc)
3  Execute the selected workflow
4  Integrate maintenance & validation
5  Review / verify / respond
`;
// Initialize MCP server with the same name as in .cursor/mcp.json
const server = new McpServer({
    name: "dss-guardrails",
    version: "1.0.0",
    description: "DSS Guardrails MCP Server"
});
// Register the guardrails tool
server.tool("dss-guardrails", async () => {
    console.error("[dss-guardrails] Tool called");
    return {
        content: [{ type: "text", text: RULES }]
    };
});
// Register a test tool
server.tool("test-tool", async () => {
    console.error("[dss-guardrails] Test tool called");
    return {
        content: [{ type: "text", text: "Test tool is working!" }]
    };
});
// Start the server
async function startServer() {
    try {
        console.error("[dss-guardrails] Starting MCP server...");
        // Create transport with explicit stdio configuration
        const transport = new StdioServerTransport();
        console.error("[dss-guardrails] Transport created");
        // Set up error handlers before connecting
        process.on('uncaughtException', (err) => {
            console.error("[dss-guardrails] Uncaught exception:", err);
            process.exit(1);
        });
        process.on('unhandledRejection', (reason, promise) => {
            console.error("[dss-guardrails] Unhandled Rejection at:", promise, "reason:", reason);
            process.exit(1);
        });
        console.error("[dss-guardrails] Connecting to transport...");
        // Connect to the transport with timeout
        const connectPromise = server.connect(transport);
        const timeoutPromise = new Promise((_, reject) => {
            setTimeout(() => reject(new Error("Connection timeout")), 5000);
        });
        await Promise.race([connectPromise, timeoutPromise]);
        console.error("[dss-guardrails] Connected to transport successfully");
        // Keep the process running
        process.on('SIGINT', () => {
            console.error("[dss-guardrails] Received SIGINT, shutting down...");
            process.exit(0);
        });
        // Handle process termination
        process.on('exit', () => {
            console.error("[dss-guardrails] Process exiting, closing transport...");
            transport.close();
        });
        // Log that we're ready to handle requests
        console.error("[dss-guardrails] Server is ready to handle requests");
    }
    catch (err) {
        console.error("[dss-guardrails] Error in startServer:", err);
        process.exit(1);
    }
}
// Start the server and handle any startup errors
console.error("[dss-guardrails] Initializing server...");
startServer().catch(err => {
    console.error("[dss-guardrails] Fatal error during startup:", err);
    process.exit(1);
});
