from __future__ import annotations

from fastapi import APIRouter

from back.schemas.models.user import UserContextResponse
from back.services.user_service import get_user_context as get_user_context_service


router = APIRouter(prefix="/api/v1/user", tags=["user"])


@router.get(
    "/context",
    response_model=UserContextResponse,
    summary="获取用户上下文",
)
async def get_user_context() -> UserContextResponse:
    """返回 Mock 的当前位置、家庭住址与用户偏好。"""

    return await get_user_context_service()
