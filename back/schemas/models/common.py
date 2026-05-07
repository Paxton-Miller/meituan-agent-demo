from __future__ import annotations

from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    """统一错误响应结构，便于 Agent 稳定解析失败原因。"""

    code: int = Field(..., description="业务或系统错误码")
    msg: str = Field(..., description="错误描述")


class Coordinate(BaseModel):
    """经纬度坐标。"""

    lat: float = Field(..., description="纬度")
    lng: float = Field(..., description="经度")
