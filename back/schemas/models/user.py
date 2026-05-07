from __future__ import annotations

from typing import Any, Dict

from pydantic import BaseModel, Field

from back.schemas.models.common import Coordinate


class UserContextResponse(BaseModel):
    current_location: Coordinate = Field(..., description="用户当前坐标")
    home_address: str = Field(..., description="家庭住址")
    user_preferences: Dict[str, Any] = Field(..., description="用户基础偏好画像")
