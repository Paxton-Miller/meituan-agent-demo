from __future__ import annotations

from typing import Dict, Iterable, List, Optional

from back.agent_tools.base import AgentTool, ToolExecutionContext
from back.agent_tools.booking import TOOLS as BOOKING_TOOLS
from back.agent_tools.poi import TOOLS as POI_TOOLS
from back.agent_tools.route import TOOLS as ROUTE_TOOLS
from back.agent_tools.user import TOOLS as USER_TOOLS
from back.services.errors import ServiceError


class ToolRegistry:
    def __init__(self, tools: Iterable[AgentTool]) -> None:
        self._tools: Dict[str, AgentTool] = {}
        for tool in tools:
            self.register(tool)

    def register(self, tool: AgentTool) -> None:
        if tool.name in self._tools:
            raise ValueError(f"重复注册工具: {tool.name}")
        self._tools[tool.name] = tool

    def get(self, name: str) -> AgentTool:
        tool = self._tools.get(name)
        if tool is None:
            raise ServiceError(status_code=404, message=f"工具不存在: {name}")
        return tool

    def list(self) -> List[AgentTool]:
        return list(self._tools.values())

    def manifest(self) -> List[dict]:
        return [tool.manifest() for tool in self.list()]

    async def invoke(
        self,
        name: str,
        arguments: Optional[dict] = None,
        context: Optional[ToolExecutionContext] = None,
    ) -> dict:
        return await self.get(name).invoke(arguments or {}, context=context)


registry = ToolRegistry(
    [
        *USER_TOOLS,
        *ROUTE_TOOLS,
        *POI_TOOLS,
        *BOOKING_TOOLS,
    ]
)
