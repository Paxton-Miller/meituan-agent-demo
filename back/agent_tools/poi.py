from __future__ import annotations

from back.agent_tools.base import AgentTool, ToolExecutionContext
from back.agent_tools.models import GetPoiStatusInput, SearchPoisInput
from back.schemas.models.poi import PoiSearchResponse, PoiStatusResponse
from back.services.poi_service import get_poi_status, search_pois


async def search_pois_handler(
    arguments: SearchPoisInput,
    _: ToolExecutionContext,
) -> PoiSearchResponse:
    return await search_pois(
        location=arguments.location,
        radius=arguments.radius,
        category=arguments.category,
        tags=arguments.tags,
    )


async def get_poi_status_handler(
    arguments: GetPoiStatusInput,
    _: ToolExecutionContext,
) -> PoiStatusResponse:
    return await get_poi_status(
        poi_id=arguments.poi_id,
        party_size=arguments.party_size,
        target_time=arguments.target_time,
    )


TOOLS = [
    AgentTool(
        name="search_pois",
        description="根据位置、业态分类和语义标签搜索本地生活 POI 候选。",
        input_model=SearchPoisInput,
        output_model=PoiSearchResponse,
        handler=search_pois_handler,
        side_effect=False,
        tags=["poi", "search", "readonly"],
    ),
    AgentTool(
        name="get_poi_status",
        description="查询 POI 的实时可预订状态、剩余容量、排队长度和等待时间。",
        input_model=GetPoiStatusInput,
        output_model=PoiStatusResponse,
        handler=get_poi_status_handler,
        side_effect=False,
        tags=["poi", "inventory", "readonly"],
    ),
]
