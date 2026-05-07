from __future__ import annotations

from typing import List

from back.agent_tools.registry import ToolRegistry, registry


def to_langchain_tools(tool_registry: ToolRegistry = registry) -> List[object]:
    """Export tools as LangChain StructuredTool objects when langchain-core is installed."""

    try:
        from langchain_core.tools import StructuredTool
    except ImportError as exc:
        raise RuntimeError("请先安装 langchain-core 才能导出 LangChain tools。") from exc

    langchain_tools: List[object] = []
    for tool in tool_registry.list():
        def build_coroutine(agent_tool):
            async def coroutine(**kwargs):
                return await agent_tool.invoke(kwargs)

            return coroutine

        langchain_tools.append(
            StructuredTool.from_function(
                name=tool.name,
                description=tool.description,
                args_schema=tool.input_model,
                coroutine=build_coroutine(tool),
            )
        )
    return langchain_tools
