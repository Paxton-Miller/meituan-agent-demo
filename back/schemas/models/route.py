from __future__ import annotations

from pydantic import BaseModel, Field

from back.schemas.enums.route import TravelMode
from back.schemas.models.common import Coordinate


class RouteEstimateResponse(BaseModel):
    origin: Coordinate = Field(..., description="起点坐标")
    destination: Coordinate = Field(..., description="终点坐标")
    travel_mode: TravelMode = Field(..., description="出行方式")
    distance_meters: int = Field(..., description="预估路线距离，单位：米")
    duration_minutes: int = Field(..., description="预估耗时，单位：分钟")
