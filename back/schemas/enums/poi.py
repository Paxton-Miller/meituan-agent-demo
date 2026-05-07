from __future__ import annotations

from enum import Enum


class POICategory(str, Enum):
    """POI 业态分类。"""

    DINING = "DINING"
    ENTERTAINMENT = "ENTERTAINMENT"
    RETAIL = "RETAIL"


class POITag(str, Enum):
    """POI 语义标签，用于约束 Agent 的搜索参数空间。"""

    KIDS_FRIENDLY = "KIDS_FRIENDLY"
    AGE_5_PLUS = "AGE_5_PLUS"
    LOW_FAT = "LOW_FAT"
    GROUP_FRIENDLY = "GROUP_FRIENDLY"
    EXHIBITION = "EXHIBITION"
    CITY_WALK = "CITY_WALK"
