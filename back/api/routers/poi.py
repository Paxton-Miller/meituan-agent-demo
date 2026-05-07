from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, Query

from back.schemas.enums.poi import POICategory, POITag
from back.schemas.models.poi import PoiSearchResponse, PoiStatusResponse
from back.services.poi_service import get_poi_status as get_poi_status_service
from back.services.poi_service import search_pois as search_pois_service


router = APIRouter(prefix="/api/v1/poi", tags=["poi"])


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
    """根据位置、业态和语义标签搜索 POI 候选。"""

    return await search_pois_service(
        location=location,
        radius=radius,
        category=category,
        tags=tags,
    )


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

    return await get_poi_status_service(
        poi_id=poi_id,
        party_size=party_size,
        target_time=target_time,
    )
