import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

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
        program_name = program_name.strip()
        response = self.call_tool(
            "get_program_info",
            {
                "program": program_name,
            },
        )

        if response.status_code != 200:
            raise ValueError(
                f"Hackenproof MCP request failed for '{program_name}' "
                f"(HTTP {response.status_code}): {response.text[:200]}"
            )

        text = response.text
        if "data:" not in text:
            raise ValueError(
                f"Unexpected Hackenproof MCP response for '{program_name}' "
                f"(no data stream): {text[:200]}"
            )

        data = text.split("data:", 1)[1].strip()
        try:
            outer = json.loads(data)
        except json.JSONDecodeError as e:
            raise ValueError(
                f"Malformed Hackenproof MCP response for '{program_name}': {data[:200]}"
            ) from e

        if isinstance(outer, dict) and outer.get("error"):
            err = outer["error"]
            msg = err.get("message", str(err)) if isinstance(err, dict) else str(err)
            raise ValueError(
                f"Program '{program_name}' not found on Hackenproof: {msg}"
            )

        try:
            content_text = outer["result"]["content"][0]["text"]
        except (KeyError, IndexError, TypeError) as e:
            raise ValueError(
                f"Malformed Hackenproof response for '{program_name}': {str(outer)[:200]}"
            ) from e

        if not isinstance(content_text, str) or not content_text.strip():
            raise ValueError(
                f"Program '{program_name}' returned empty content from Hackenproof"
            )

        lowered = content_text.strip().lower()
        not_found_markers = (
            "not found",
            "does not exist",
            "no such program",
            "program not found",
        )
        if lowered.startswith(not_found_markers) or len(lowered) < 40 and any(m in lowered for m in not_found_markers):
            raise ValueError(
                f"Program '{program_name}' not found on Hackenproof: {content_text.strip()[:200]}"
            )

        return content_text


_client: HackenProofMCP | None = None


def _get_client() -> HackenProofMCP:
    global _client
    if _client is None:
        api_key = os.getenv("HACKENPROOF_API_KEY")
        if not api_key:
            raise ValueError(
                "HACKENPROOF_API_KEY not found. Set it in .env (local) or "
                "in Streamlit Cloud Secrets (HACKENPROOF_API_KEY)."
            )
        _client = HackenProofMCP(api_key)
    return _client


def hackenproof_data(program_name: str):
    return _get_client().get_program_info(program_name)