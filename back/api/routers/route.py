from __future__ import annotations

from fastapi import APIRouter, Query

from back.schemas.enums.route import TravelMode
from back.schemas.models.route import RouteEstimateResponse
from back.services.route_service import estimate_route as estimate_route_service


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

    return await estimate_route_service(
        origin_lat=origin_lat,
        origin_lng=origin_lng,
        dest_lat=dest_lat,
        dest_lng=dest_lng,
        travel_mode=travel_mode,
    )
