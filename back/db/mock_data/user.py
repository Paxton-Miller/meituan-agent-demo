from __future__ import annotations

from typing import Any, Dict

from back.schemas.enums.poi import POITag


# Mock 用户上下文：模拟 App 已知的用户基础信息。真实系统中通常来自登录态、
# 用户画像服务、家庭地址簿和历史偏好。这里选择上海静安附近作为基准点，
# 方便测试亲子、轻食、周末活动等典型本地生活规划场景。
MOCK_USER_CONTEXT: Dict[str, Any] = {
    "current_location": {"lat": 31.2304, "lng": 121.4737},
    "home_address": "上海市静安区南京西路 1266 号",
    "user_preferences": {
        "family_members": ["2 位成人", "1 位 5 岁儿童"],
        "preferred_tags": [POITag.KIDS_FRIENDLY, POITag.AGE_5_PLUS, POITag.LOW_FAT],
        "avoid_tags": ["重油", "排队过长", "过度刺激"],
        "budget_per_person": 180,
    },
}
