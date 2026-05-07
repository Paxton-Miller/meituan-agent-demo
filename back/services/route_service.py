from __future__ import annotations

from back.schemas.enums.route import TravelMode
from back.schemas.models.common import Coordinate
from back.schemas.models.route import RouteEstimateResponse
from back.utils.geo_utils import calculate_distance_meters, estimate_duration_minutes


async def estimate_route(
    origin_lat: float,
    origin_lng: float,
    dest_lat: float,
    dest_lng: float,
    travel_mode: TravelMode = TravelMode.TAXI,
) -> RouteEstimateResponse:
    distance_meters = calculate_distance_meters(origin_lat, origin_lng, dest_lat, dest_lng)
    duration_minutes = estimate_duration_minutes(distance_meters, travel_mode)

    return RouteEstimateResponse(
        origin=Coordinate(lat=origin_lat, lng=origin_lng),
        destination=Coordinate(lat=dest_lat, lng=dest_lng),
        travel_mode=travel_mode,
        distance_meters=distance_meters,
        duration_minutes=duration_minutes,
    )
