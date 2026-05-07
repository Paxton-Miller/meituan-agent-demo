from __future__ import annotations

import json
from typing import Any, Dict, Optional
from urllib import request


class ToolServiceClient:
    """Small dependency-free HTTP client for internal agent platforms."""

    def __init__(self, base_url: str, timeout: float = 10.0) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def list_tools(self) -> Dict[str, Any]:
        return self._json_request("GET", "/api/v1/tools")

    def call_tool(
        self,
        name: str,
        arguments: Optional[Dict[str, Any]] = None,
        request_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        headers = {}
        if request_id:
            headers["X-Request-ID"] = request_id
        return self._json_request(
            "POST",
            "/api/v1/tools/call",
            body={"name": name, "arguments": arguments or {}},
            headers=headers,
        )

    def _json_request(
        self,
        method: str,
        path: str,
        body: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        data = None
        request_headers = {"Accept": "application/json", **(headers or {})}
        if body is not None:
            data = json.dumps(body).encode("utf-8")
            request_headers["Content-Type"] = "application/json"

        req = request.Request(
            f"{self.base_url}{path}",
            data=data,
            headers=request_headers,
            method=method,
        )
        with request.urlopen(req, timeout=self.timeout) as response:
            return json.loads(response.read().decode("utf-8"))
