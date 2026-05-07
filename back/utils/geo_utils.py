from __future__ import annotations

import math

from back.schemas.enums.route import TravelMode


def calculate_distance_meters(
    origin_lat: float,
    origin_lng: float,
    dest_lat: float,
    dest_lng: float,
) -> int:
    """使用 Haversine 公式计算经纬度直线距离，并乘以路线绕行系数得到 Mock 路线距离。"""

    earth_radius_meters = 6_371_000
    lat1 = math.radians(origin_lat)
    lat2 = math.radians(dest_lat)
    delta_lat = math.radians(dest_lat - origin_lat)
    delta_lng = math.radians(dest_lng - origin_lng)

    a = (
        math.sin(delta_lat / 2) ** 2
        + math.cos(lat1) * math.cos(lat2) * math.sin(delta_lng / 2) ** 2
    )
    straight_distance = earth_radius_meters * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    route_factor = 1.28
    return int(straight_distance * route_factor)


def estimate_duration_minutes(distance_meters: int, travel_mode: TravelMode) -> int:
    """根据交通方式使用固定平均速度估算耗时。"""

    speed_km_per_hour = {
        TravelMode.WALKING: 4.5,
        TravelMode.TAXI: 28.0,
    }[travel_mode]
    minutes = (distance_meters / 1000) / speed_km_per_hour * 60
    return max(1, math.ceil(minutes))
