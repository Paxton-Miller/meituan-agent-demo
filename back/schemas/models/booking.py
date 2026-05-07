from __future__ import annotations

from pydantic import BaseModel, Field

from back.schemas.enums.booking import OrderStatus


class OrderRecord(BaseModel):
    """内存订单记录，用于模拟交易执行后的状态持久化。"""

    order_id: str = Field(..., description="订单号")
    poi_id: str = Field(..., description="被预订的 POI ID")
    party_size: int = Field(..., description="出行/用餐人数")
    reserve_time: str = Field(..., description="预订时间")
    status: OrderStatus = Field(..., description="订单状态")
    created_at: str = Field(..., description="订单创建时间")


class ReserveRequest(BaseModel):
    poi_id: str = Field(..., description="需要预订的 POI ID", examples=["poi_science_kids_001"])
    party_size: int = Field(..., ge=1, le=20, description="预订人数")
    reserve_time: str = Field(
        ...,
        description="预订时间，建议使用 ISO 8601 格式",
        examples=["2026-05-09T14:00:00+08:00"],
    )


class ReserveResponse(BaseModel):
    success: bool = Field(..., description="是否预订成功")
    order_id: str = Field(..., description="生成的订单号")
    poi_id: str = Field(..., description="被预订的 POI ID")
    reserve_time: str = Field(..., description="预订时间")
    status: OrderStatus = Field(..., description="订单状态")
    msg: str = Field(..., description="预订结果描述")
