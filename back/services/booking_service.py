from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional

from back.db.mock_data.booking import MOCK_ORDERS
from back.db.mock_data.poi import MOCK_INVENTORY
from back.schemas.enums.booking import OrderStatus
from back.schemas.models.booking import OrderRecord, ReserveRequest, ReserveResponse
from back.services.errors import ServiceError
from back.services.poi_service import get_poi_or_raise


async def reserve_booking(
    request: ReserveRequest,
    idempotency_key: Optional[str] = None,
) -> ReserveResponse:
    get_poi_or_raise(request.poi_id)
    inventory = MOCK_INVENTORY.get(request.poi_id)
    if inventory is None:
        raise ServiceError(status_code=404, message=f"库存状态不存在: {request.poi_id}")
    if not inventory.is_bookable:
        raise ServiceError(status_code=409, message="当前 POI 不可预订")
    if inventory.remaining_capacity < request.party_size:
        raise ServiceError(status_code=409, message="剩余容量不足，无法完成预订")

    order_id = f"order_{uuid.uuid4().hex}"
    if idempotency_key:
        order_id = f"order_{idempotency_key}"
        existing_order = MOCK_ORDERS.get(order_id)
        if existing_order is not None:
            return ReserveResponse(
                success=True,
                order_id=existing_order.order_id,
                poi_id=existing_order.poi_id,
                reserve_time=existing_order.reserve_time,
                status=existing_order.status,
                msg="预订成功（幂等返回）",
            )

    order = OrderRecord(
        order_id=order_id,
        poi_id=request.poi_id,
        party_size=request.party_size,
        reserve_time=request.reserve_time,
        status=OrderStatus.RESERVED,
        created_at=datetime.utcnow().isoformat(),
    )
    MOCK_ORDERS[order_id] = order

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
