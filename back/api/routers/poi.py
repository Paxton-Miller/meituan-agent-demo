from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, HTTPException, Query

from back.db.mock_data.poi import MOCK_INVENTORY, MOCK_POIS, get_poi_or_404
from back.schemas.enums.poi import POICategory, POITag
from back.schemas.models.poi import InventoryStatus, PoiItem, PoiSearchResponse, PoiStatusResponse


router = APIRouter(prefix="/api/v1/poi", tags=["poi"])


def build_status_hint(inventory: InventoryStatus, party_size: int) -> str:
    """把库存字段转成 Agent 易理解的自然语言提示。"""

    if not inventory.is_bookable:
        return "当前不可预订，建议选择其他时间或替代 POI。"
    if inventory.remaining_capacity < party_size:
        return "剩余容量不足，无法满足当前人数。"
    if inventory.estimated_wait_time > 30:
        return "可预订但等待时间较长，建议作为备选方案。"
    return "当前状态良好，适合加入行程计划。"


@router.get(
    "/search",
    response_model=PoiSearchResponse,
    summary="根据标签搜索 POI",
)
async def search_pois(
    location: Optional[str] = Query(
        None,
        description="语义化位置描述，例如 上海静安、人民广场；Mock 版本仅保留字段方便 Agent 传参",
    ),
    radius: int = Query(5000, ge=100, le=50000, description="搜索半径，单位：米"),
    category: Optional[POICategory] = Query(None, description="POI 业态分类"),
    tags: Optional[List[POITag]] = Query(
        None,
        description=(
            "关键语义标签，可重复传入，例如 "
            "tags=KIDS_FRIENDLY&tags=AGE_5_PLUS"
        ),
    ),
) -> PoiSearchResponse:
    """遍历 MOCK_POIS，根据输入 tags 和 POI 标签的交集进行过滤。"""

    required_tags = set(tags or [])

    # Mock 版本不做真实地理围栏过滤，保留 location/radius 是为了让接口形态贴近真实搜索服务。
    matched_pois: List[PoiItem] = []
    for poi in MOCK_POIS:
        if category is not None and poi.category != category:
            continue
        if required_tags and not (required_tags & set(poi.tags)):
            continue
        matched_pois.append(poi)

    # 如果没有传入 category 和 tags，则默认返回全部 POI，便于 Agent 在探索阶段获取候选池。
    return PoiSearchResponse(total=len(matched_pois), items=matched_pois)


@router.get(
    "/status",
    response_model=PoiStatusResponse,
    summary="查询 POI 实时状态与库存",
)
async def get_poi_status(
    poi_id: str = Query(..., description="POI 唯一标识"),
    party_size: int = Query(..., ge=1, le=20, description="人数"),
    target_time: Optional[str] = Query(None, description="目标到店或入场时间，建议 ISO 8601 格式"),
) -> PoiStatusResponse:
    """根据 poi_id 查询排队、等待时间和可预订状态。"""

    get_poi_or_404(poi_id)
    inventory = MOCK_INVENTORY.get(poi_id)
    if inventory is None:
        raise HTTPException(status_code=404, detail=f"库存状态不存在: {poi_id}")

    effective_bookable = inventory.is_bookable and inventory.remaining_capacity >= party_size
    return PoiStatusResponse(
        poi_id=poi_id,
        party_size=party_size,
        target_time=target_time,
        is_bookable=effective_bookable,
        current_queue_length=inventory.current_queue_length,
        estimated_wait_time=inventory.estimated_wait_time,
        remaining_capacity=inventory.remaining_capacity,
        status_hint=build_status_hint(inventory, party_size),
    )
