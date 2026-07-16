import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("HACKENPROOF_API_KEY")
MCP_URL = "https://mcp.hackenproof.com/mcp"


class HackenProofMCP:
    def __init__(self, api_key: str):
        self.url = MCP_URL
        self.request_id = 1

        self.headers = {
            "X-Api-Key": api_key,
            "Accept": "application/json, text/event-stream",
            "Content-Type": "application/json",
        }

        self.session_id = None
        self.initialize()

    def _request(self, method: str, params: dict | None = None):
        payload = {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": method,
            "params": params or {},
        }

        self.request_id += 1

        return requests.post(
            self.url,
            headers=self.headers,
            json=payload,
        )

    def initialize(self):
        response = self._request(
            "initialize",
            {
                "protocolVersion": "2025-03-26",
                "capabilities": {},
                "clientInfo": {
                    "name": "WiseHat",
                    "version": "0.1.0",
                },
            },
        )

        if response.status_code != 200:
            raise RuntimeError(
                f"Initialization failed:\n{response.text}"
            )

        self.session_id = response.headers.get("Mcp-Session-Id")

        if self.session_id:
            self.headers["Mcp-Session-Id"] = self.session_id

    def call_tool(self, tool_name: str, arguments: dict):
        return self._request(
            "tools/call",
            {
                "name": tool_name,
                "arguments": arguments,
            },
        )


    def get_program_info(self, program_name: str):
        response = self.call_tool(
            "get_program_info",
            {
                "program": program_name,
            },
        )

        data = response.text.split("data:", 1)[1].strip()
        outer = json.loads(data)

        return outer["result"]["content"][0]["text"]


if not API_KEY:
    raise ValueError("HACKENPROOF_API_KEY not found in .env")

# Create one client when this module is imported
client = HackenProofMCP(API_KEY)


def hackenproof_data(program_name: str):
    return client.get_program_info(program_name)