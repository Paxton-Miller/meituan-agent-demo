from __future__ import annotations


class ServiceError(Exception):
    """Domain-level error that can be mapped to HTTP, MCP, or agent runtime failures."""

    def __init__(self, status_code: int, message: str) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.message = message
