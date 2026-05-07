from __future__ import annotations

from back.agent_tools.base import AgentTool, ToolExecutionContext
from back.agent_tools.models import ReserveBookingInput
from back.schemas.models.booking import ReserveRequest, ReserveResponse
from back.services.booking_service import reserve_booking


async def reserve_booking_handler(
    arguments: ReserveBookingInput,
    _: ToolExecutionContext,
) -> ReserveResponse:
    request = ReserveRequest(
        poi_id=arguments.poi_id,
        party_size=arguments.party_size,
        reserve_time=arguments.reserve_time,
    )
    return await reserve_booking(request=request, idempotency_key=arguments.idempotency_key)


TOOLS = [
    AgentTool(
        name="reserve_booking",
        description="在用户确认后创建 POI 预订订单，并扣减 mock 库存。",
        input_model=ReserveBookingInput,
        output_model=ReserveResponse,
        handler=reserve_booking_handler,
        side_effect=True,
        idempotent=False,
        tags=["booking", "transaction", "write"],
    )
]
