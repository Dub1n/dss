import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

async function startServer() {
  try {
    // Create a simple server
    const server = new McpServer({ 
      name: "dss-guardrails", 
      version: "1.0.0" 
    });

    // Register a simple test tool
    server.tool("test", async () => {
      return { content: [{ type: "text", text: "Hello from MCP!" }] };
    });

    // Start the server
    console.error("[minimal] Starting server...");
    const transport = new StdioServerTransport();
    await server.connect(transport);
    console.error("[minimal] Server connected successfully");

    // Keep the process running
    process.on('SIGINT', () => {
      console.error("[minimal] Shutting down...");
      process.exit(0);
    });
  } catch (error) {
    console.error("[minimal] Error starting server:", error);
    process.exit(1);
  }
}

startServer().catch(error => {
  console.error("[minimal] Fatal error:", error);
  process.exit(1);
}); 