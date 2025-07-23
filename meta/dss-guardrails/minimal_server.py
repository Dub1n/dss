import sys
import json
import asyncio
import logging
from typing import Dict, Any, List

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    handlers=[logging.StreamHandler(sys.stderr)]
)
logger = logging.getLogger('dss-guardrails')

class MinimalMcpServer:
    def __init__(self):
        self.name = "dss-guardrails"
        self.version = "1.0.0"
        self.tools = {}
        logger.info(f"Initializing {self.name} server v{self.version}")
        self.register_tools()

    def register_tools(self):
        logger.debug("Registering tools...")
        async def test_tool() -> Dict[str, Any]:
            logger.debug("Test tool called")
            return {
                "content": [{"type": "text", "text": "Hello from MCP!"}]
            }
        self.tools["test"] = test_tool
        logger.info(f"Registered tools: {list(self.tools.keys())}")

    async def handle_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        try:
            logger.debug(f"Received message: {message}")
            if message.get("type") == "tool_call":
                tool_name = message.get("name")
                logger.debug(f"Tool call for: {tool_name}")
                if tool_name in self.tools:
                    result = await self.tools[tool_name]()
                    logger.debug(f"Tool result: {result}")
                    return {
                        "type": "tool_result",
                        "id": message.get("id"),
                        "result": result
                    }
            logger.warning(f"Unknown message type or tool: {message}")
            return {
                "type": "error",
                "error": f"Unknown message type or tool: {message}"
            }
        except Exception as e:
            logger.error(f"Error handling message: {e}", exc_info=True)
            return {
                "type": "error",
                "error": str(e)
            }

    async def run(self):
        logger.info("Starting server...")
        
        while True:
            try:
                # Read message from stdin
                line = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
                if not line:
                    logger.warning("Received empty line, breaking loop")
                    break
                
                logger.debug(f"Raw input: {line.strip()}")
                message = json.loads(line)
                response = await self.handle_message(message)
                
                # Write response to stdout
                response_str = json.dumps(response)
                logger.debug(f"Sending response: {response_str}")
                print(response_str, flush=True)
                
            except json.JSONDecodeError as e:
                logger.error(f"JSON decode error: {e}")
                print(json.dumps({
                    "type": "error",
                    "error": "Invalid JSON received"
                }), flush=True)
            except Exception as e:
                logger.error(f"Unexpected error: {e}", exc_info=True)
                print(json.dumps({
                    "type": "error",
                    "error": str(e)
                }), flush=True)

async def main():
    try:
        logger.info("Starting main...")
        server = MinimalMcpServer()
        await server.run()
    except Exception as e:
        logger.error(f"Fatal error in main: {e}", exc_info=True)
        raise

if __name__ == "__main__":
    try:
        logger.info("Script started")
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Shutting down...")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1) 