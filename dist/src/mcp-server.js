import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
process.env.DEBUG = '*';
const server = new McpServer({
    name: "my-mcp-server",
    version: "1.0.0",
    description: "My MCP Server for DSS"
});
server.tool("test", async () => {
    return { content: [{ type: "text", text: "Hello from MCP!" }] };
});
async function startServer() {
    try {
        const transport = new StdioServerTransport();
        await server.connect(transport);
        console.error("[mcp-server] Connected and ready.");
    }
    catch (err) {
        console.error("[mcp-server] Error in startServer:", err);
        process.exit(1);
    }
}
startServer();
