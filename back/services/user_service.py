from __future__ import annotations

from back.db.mock_data.user import MOCK_USER_CONTEXT
from back.schemas.models.user import UserContextResponse


async def get_user_context() -> UserContextResponse:
    return UserContextResponse(**MOCK_USER_CONTEXT)
