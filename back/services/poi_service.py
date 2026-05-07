from __future__ import annotations

from typing import List, Optional

from back.db.mock_data.poi import MOCK_INVENTORY, MOCK_POIS
from back.schemas.enums.poi import POICategory, POITag
from back.schemas.models.poi import InventoryStatus, PoiItem, PoiSearchResponse, PoiStatusResponse
from back.services.errors import ServiceError


def get_poi_or_raise(poi_id: str) -> PoiItem:
    for poi in MOCK_POIS:
        if poi.poi_id == poi_id:
            return poi
    raise ServiceError(status_code=404, message=f"POI 不存在: {poi_id}")


def build_status_hint(inventory: InventoryStatus, party_size: int) -> str:
    if not inventory.is_bookable:
        return "当前不可预订，建议选择其他时间或替代 POI。"
    if inventory.remaining_capacity < party_size:
        return "剩余容量不足，无法满足当前人数。"
    if inventory.estimated_wait_time > 30:
        return "可预订但等待时间较长，建议作为备选方案。"
    return "当前状态良好，适合加入行程计划。"


async def search_pois(
    location: Optional[str] = None,
    radius: int = 5000,
    category: Optional[POICategory] = None,
    tags: Optional[List[POITag]] = None,
) -> PoiSearchResponse:
    required_tags = set(tags or [])

    matched_pois: List[PoiItem] = []
    for poi in MOCK_POIS:
        if category is not None and poi.category != category:
            continue
        if required_tags and not (required_tags & set(poi.tags)):
            continue
        matched_pois.append(poi)

    return PoiSearchResponse(total=len(matched_pois), items=matched_pois)


async def get_poi_status(
    poi_id: str,
    party_size: int,
    target_time: Optional[str] = None,
) -> PoiStatusResponse:
    get_poi_or_raise(poi_id)
    inventory = MOCK_INVENTORY.get(poi_id)
    if inventory is None:
        raise ServiceError(status_code=404, message=f"库存状态不存在: {poi_id}")

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
