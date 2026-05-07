from __future__ import annotations

from typing import Dict

from back.schemas.models.booking import OrderRecord


# Mock 订单表：服务启动时为空；每次调用预订接口后写入一条订单记录。
# 真实生产环境中这里会替换为订单数据库、消息队列和交易一致性处理。
MOCK_ORDERS: Dict[str, OrderRecord] = {}
