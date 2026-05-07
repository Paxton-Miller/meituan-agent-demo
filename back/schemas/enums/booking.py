from __future__ import annotations

from enum import Enum


class OrderStatus(str, Enum):
    """订单状态。"""

    PENDING = "PENDING"
    RESERVED = "RESERVED"
    DELIVERING = "DELIVERING"
