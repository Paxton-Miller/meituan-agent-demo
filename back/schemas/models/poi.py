from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field

from back.schemas.enums.poi import POICategory, POITag
from back.schemas.models.common import Coordinate


class PoiItem(BaseModel):
    """POI 基础信息。"""

    poi_id: str = Field(..., description="POI 唯一标识")
    name: str = Field(..., description="POI 名称")
    category: POICategory = Field(..., description="POI 业态分类")
    address: str = Field(..., description="详细地址")
    location: Coordinate = Field(..., description="POI 坐标")
    tags: List[POITag] = Field(..., description="适合 Agent 检索和推荐的语义标签")
    rating: float = Field(..., description="评分，满分 5 分")
    avg_price: int = Field(..., description="人均价格，单位：元")
    opening_hours: str = Field(..., description="营业时间描述")
    description: str = Field(..., description="面向用户可展示的 POI 简介")


class InventoryStatus(BaseModel):
    """POI 的实时库存、排队与预订状态。"""

    poi_id: str = Field(..., description="POI 唯一标识")
    is_bookable: bool = Field(..., description="当前是否可预订")
    current_queue_length: int = Field(..., description="当前排队桌数或排队批次")
    estimated_wait_time: int = Field(..., description="预计等待时间，单位：分钟")
    remaining_capacity: int = Field(..., description="剩余可接待人数或票量")
    updated_at: str = Field(..., description="状态更新时间，ISO 8601 字符串")


class PoiSearchResponse(BaseModel):
    total: int = Field(..., description="匹配 POI 总数")
    items: List[PoiItem] = Field(..., description="匹配的 POI 列表")


class PoiStatusResponse(BaseModel):
    poi_id: str = Field(..., description="POI 唯一标识")
    party_size: int = Field(..., description="查询人数")
    target_time: Optional[str] = Field(None, description="目标到店或入场时间")
    is_bookable: bool = Field(..., description="是否可预订")
    current_queue_length: int = Field(..., description="当前排队桌数或批次")
    estimated_wait_time: int = Field(..., description="预计等待时间，单位：分钟")
    remaining_capacity: int = Field(..., description="剩余可接待人数或票量")
    status_hint: str = Field(..., description="给 Agent/用户的状态解释")
