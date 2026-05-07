from __future__ import annotations

from typing import Any, Dict, Optional

from fastapi import APIRouter, Header
from pydantic import BaseModel, Field

from back.agent_tools.adapters.openai_tools import to_openai_tools
from back.agent_tools.base import ToolExecutionContext
from back.agent_tools.registry import registry


router = APIRouter(prefix="/api/v1/tools", tags=["tools"])


class ToolCallRequest(BaseModel):
    name: str = Field(..., description="工具名称。")
    arguments: Dict[str, Any] = Field(default_factory=dict, description="工具入参。")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="调用方附加上下文。")


class ToolCallResponse(BaseModel):
    name: str
    result: Dict[str, Any]


@router.get("", summary="列出 Agent 工具清单")
async def list_tools() -> Dict[str, Any]:
    return {"tools": registry.manifest()}


@router.get("/openai", summary="导出 OpenAI function tools")
async def list_openai_tools(strict: bool = False) -> Dict[str, Any]:
    return {"tools": to_openai_tools(registry, strict=strict)}


@router.post("/call", response_model=ToolCallResponse, summary="通过 HTTP 调用工具")
async def call_tool(
    request: ToolCallRequest,
    request_id: Optional[str] = Header(None, alias="X-Request-ID"),
    actor: Optional[str] = Header(None, alias="X-Actor"),
) -> ToolCallResponse:
    context = ToolExecutionContext(
        request_id=request_id,
        actor=actor,
        metadata=request.metadata,
    )
    result = await registry.invoke(request.name, request.arguments, context=context)
    return ToolCallResponse(name=request.name, result=result)
