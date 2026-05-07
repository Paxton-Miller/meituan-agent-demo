from __future__ import annotations

from typing import Any, Dict, List

from back.agent_tools.registry import ToolRegistry, registry


def to_openai_tools(
    tool_registry: ToolRegistry = registry,
    strict: bool = False,
) -> List[Dict[str, Any]]:
    """Export tools in the OpenAI Chat Completions/Responses function-tool shape."""

    tools: List[Dict[str, Any]] = []
    for tool in tool_registry.list():
        function: Dict[str, Any] = {
            "name": tool.name,
            "description": tool.description,
            "parameters": tool.input_schema,
        }
        if strict:
            function["strict"] = True
        tools.append({"type": "function", "function": function})
    return tools
