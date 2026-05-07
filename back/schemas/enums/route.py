from __future__ import annotations

from enum import Enum


class TravelMode(str, Enum):
    """路线规划出行方式。"""

    WALKING = "WALKING"
    TAXI = "TAXI"
