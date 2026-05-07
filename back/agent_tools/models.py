from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field

from back.schemas.enums.poi import POICategory, POITag
from back.schemas.enums.route import TravelMode


class EmptyInput(BaseModel):
    """No arguments are required."""


class SearchPoisInput(BaseModel):
    location: Optional[str] = Field(
        None,
        description="语义化位置描述，例如 上海静安、人民广场。",
    )
    radius: int = Field(5000, ge=100, le=50000, description="搜索半径，单位：米。")
    category: Optional[POICategory] = Field(None, description="POI 业态分类。")
    tags: Optional[List[POITag]] = Field(
        None,
        description="关键语义标签，例如 KIDS_FRIENDLY、LOW_FAT。",
    )


class GetPoiStatusInput(BaseModel):
    poi_id: str = Field(..., description="POI 唯一标识。")
    party_size: int = Field(..., ge=1, le=20, description="人数。")
    target_time: Optional[str] = Field(None, description="目标到店或入场时间，建议 ISO 8601。")


class EstimateRouteInput(BaseModel):
    origin_lat: float = Field(..., description="起点纬度。")
    origin_lng: float = Field(..., description="起点经度。")
    dest_lat: float = Field(..., description="终点纬度。")
    dest_lng: float = Field(..., description="终点经度。")
    travel_mode: TravelMode = Field(TravelMode.TAXI, description="出行方式。")


class ReserveBookingInput(BaseModel):
    poi_id: str = Field(..., description="需要预订的 POI ID。")
    party_size: int = Field(..., ge=1, le=20, description="预订人数。")
    reserve_time: str = Field(..., description="预订时间，建议 ISO 8601。")
    idempotency_key: Optional[str] = Field(
        None,
        description="幂等键；生产环境建议每次用户确认下单动作固定一个值。",
    )
