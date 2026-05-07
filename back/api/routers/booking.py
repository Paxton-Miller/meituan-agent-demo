from __future__ import annotations

import uuid
from datetime import datetime

from fastapi import APIRouter, HTTPException

from back.db.mock_data.booking import MOCK_ORDERS
from back.db.mock_data.poi import MOCK_INVENTORY, get_poi_or_404
from back.schemas.enums.booking import OrderStatus
from back.schemas.models.booking import OrderRecord, ReserveRequest, ReserveResponse


router = APIRouter(prefix="/api/v1/booking", tags=["booking"])


@router.post(
    "/reserve",
    response_model=ReserveResponse,
    summary="创建预订订单",
)
async def reserve_booking(request: ReserveRequest) -> ReserveResponse:
    """校验库存后创建 Mock 订单，并扣减对应 POI 的剩余容量。"""

    get_poi_or_404(request.poi_id)
    inventory = MOCK_INVENTORY.get(request.poi_id)
    if inventory is None:
        raise HTTPException(status_code=404, detail=f"库存状态不存在: {request.poi_id}")
    if not inventory.is_bookable:
        raise HTTPException(status_code=409, detail="当前 POI 不可预订")
    if inventory.remaining_capacity < request.party_size:
        raise HTTPException(status_code=409, detail="剩余容量不足，无法完成预订")

    order_id = f"order_{uuid.uuid4().hex}"
    order = OrderRecord(
        order_id=order_id,
        poi_id=request.poi_id,
        party_size=request.party_size,
        reserve_time=request.reserve_time,
        status=OrderStatus.RESERVED,
        created_at=datetime.utcnow().isoformat(),
    )
    MOCK_ORDERS[order_id] = order

    # Mock 扣库存：真实系统需要事务、幂等键、库存冻结和支付状态机；
    # 这里直接减少 remaining_capacity，便于在连续接口调用中观察状态变化。
    inventory.remaining_capacity -= request.party_size
    inventory.updated_at = datetime.utcnow().isoformat()
    if inventory.remaining_capacity <= 0:
        inventory.is_bookable = False

    return ReserveResponse(
        success=True,
        order_id=order_id,
        poi_id=request.poi_id,
        reserve_time=request.reserve_time,
        status=OrderStatus.RESERVED,
        msg="预订成功",
    )
