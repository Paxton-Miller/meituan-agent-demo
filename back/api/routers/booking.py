from __future__ import annotations

from fastapi import APIRouter, Header

from back.schemas.models.booking import ReserveRequest, ReserveResponse
from back.services.booking_service import reserve_booking as reserve_booking_service


router = APIRouter(prefix="/api/v1/booking", tags=["booking"])


@router.post(
    "/reserve",
    response_model=ReserveResponse,
    summary="创建预订订单",
)
async def reserve_booking(
    request: ReserveRequest,
    idempotency_key: str | None = Header(None, alias="Idempotency-Key"),
) -> ReserveResponse:
    """校验库存后创建 Mock 订单，并扣减对应 POI 的剩余容量。"""

    return await reserve_booking_service(request=request, idempotency_key=idempotency_key)
