from __future__ import annotations

from fastapi import APIRouter, Query

from back.schemas.enums.route import TravelMode
from back.schemas.models.common import Coordinate
from back.schemas.models.route import RouteEstimateResponse
from back.utils.geo_utils import calculate_distance_meters, estimate_duration_minutes


router = APIRouter(prefix="/api/v1/route", tags=["route"])


@router.get(
    "/estimate",
    response_model=RouteEstimateResponse,
    summary="估算两点间距离与耗时",
)
async def estimate_route(
    origin_lat: float = Query(..., description="起点纬度"),
    origin_lng: float = Query(..., description="起点经度"),
    dest_lat: float = Query(..., description="终点纬度"),
    dest_lng: float = Query(..., description="终点经度"),
    travel_mode: TravelMode = Query(TravelMode.TAXI, description="出行方式"),
) -> RouteEstimateResponse:
    """使用经纬度距离和固定速度进行 Mock 路线估算。"""

    distance_meters = calculate_distance_meters(origin_lat, origin_lng, dest_lat, dest_lng)
    duration_minutes = estimate_duration_minutes(distance_meters, travel_mode)

    return RouteEstimateResponse(
        origin=Coordinate(lat=origin_lat, lng=origin_lng),
        destination=Coordinate(lat=dest_lat, lng=dest_lng),
        travel_mode=travel_mode,
        distance_meters=distance_meters,
        duration_minutes=duration_minutes,
    )
