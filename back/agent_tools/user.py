from __future__ import annotations

from back.agent_tools.base import AgentTool, ToolExecutionContext
from back.agent_tools.models import EmptyInput
from back.schemas.models.user import UserContextResponse
from back.services.user_service import get_user_context


async def get_user_context_handler(
    _: EmptyInput,
    __: ToolExecutionContext,
) -> UserContextResponse:
    return await get_user_context()


TOOLS = [
    AgentTool(
        name="get_user_context",
        description="获取当前用户位置、家庭地址和基础偏好画像。",
        input_model=EmptyInput,
        output_model=UserContextResponse,
        handler=get_user_context_handler,
        side_effect=False,
        tags=["user", "context", "readonly"],
    )
]
