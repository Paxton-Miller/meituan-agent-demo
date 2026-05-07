from __future__ import annotations

from back.agent_tools.base import AgentTool, ToolExecutionContext
from back.agent_tools.models import EstimateRouteInput
from back.schemas.models.route import RouteEstimateResponse
from back.services.route_service import estimate_route


async def estimate_route_handler(
    arguments: EstimateRouteInput,
    _: ToolExecutionContext,
) -> RouteEstimateResponse:
    return await estimate_route(
        origin_lat=arguments.origin_lat,
        origin_lng=arguments.origin_lng,
        dest_lat=arguments.dest_lat,
        dest_lng=arguments.dest_lng,
        travel_mode=arguments.travel_mode,
    )


TOOLS = [
    AgentTool(
        name="estimate_route",
        description="估算两个坐标点之间的路线距离和出行耗时。",
        input_model=EstimateRouteInput,
        output_model=RouteEstimateResponse,
        handler=estimate_route_handler,
        side_effect=False,
        tags=["route", "readonly"],
    )
]
