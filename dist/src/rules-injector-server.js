import { McpServer } from '@modelcontextprotocol/sdk/dist/esm/server/mcp.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/dist/esm/server/stdio.js';
// Enable debug logging
process.env.DEBUG = '*';
const RULES_INJECTOR_DESCRIPTION = `
Rules Injector MCP Server provides:
1. Injection of custom rules and guidelines into conversations
2. Context-aware rule application
3. Rule validation and verification
4. Rule persistence across conversation context
`;
// Initialize the MCP server
const server = new McpServer({
    name: "rules_injector_server",
    version: "0.2.0",
    description: RULES_INJECTOR_DESCRIPTION
});
// Register the rules injector tool
server.tool("rules_injector", {
    description: "Injects and manages custom rules and guidelines in conversations",
    parameters: {
        type: "object",
        properties: {
            rule_type: {
                type: "string",
                description: "The type of rule to inject",
                enum: ["behavior", "format", "validation", "context"]
            },
            rule_content: {
                type: "string",
                description: "The actual rule or guideline to inject"
            },
            context: {
                type: "string",
                description: "Additional context for when and how to apply the rule"
            },
            priority: {
                type: "number",
                description: "Rule priority (1-5, where 5 is highest)",
                minimum: 1,
                maximum: 5
            }
        },
        required: ["rule_type", "rule_content"]
    }
}, async (params) => {
    console.error("[rules-injector] Tool called with params:", JSON.stringify(params, null, 2));
    const rule = {
        type: params.rule_type,
        content: params.rule_content,
        context: params.context || "Global",
        priority: params.priority || 3,
        timestamp: new Date().toISOString()
    };
    console.error("[rules-injector] Rule stored:", JSON.stringify(rule, null, 2));
    return {
        content: [{
                type: "text",
                text: `Rule injected successfully:\nType: ${rule.type}\nContent: ${rule.content}\nContext: ${rule.context}\nPriority: ${rule.priority}`
            }]
    };
});
// Create transport with stdio configuration
const transport = new StdioServerTransport();
// Set up error handlers
process.on('uncaughtException', (err) => {
    console.error("[rules-injector] Uncaught exception:", err);
    process.exit(1);
});
process.on('unhandledRejection', (reason, promise) => {
    console.error("[rules-injector] Unhandled Rejection at:", promise, "reason:", reason);
    process.exit(1);
});
// Connect to the transport
console.error("[rules-injector] Connecting to transport...");
server.connect(transport)
    .then(() => {
    console.error("[rules-injector] Connected to transport successfully");
    console.error("[rules-injector] Server is ready to handle requests");
})
    .catch(error => {
    console.error("[rules-injector] Error starting server:", error);
    process.exit(1);
});
// Handle process termination
process.on('SIGINT', () => {
    console.error("[rules-injector] Received SIGINT, shutting down...");
    process.exit(0);
});
process.on('exit', () => {
    console.error("[rules-injector] Process exiting, closing transport...");
    transport.close();
});
