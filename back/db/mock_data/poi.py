from __future__ import annotations

from datetime import datetime
from typing import Dict, List

from fastapi import HTTPException

from back.schemas.enums.poi import POICategory, POITag
from back.schemas.models.common import Coordinate
from back.schemas.models.poi import InventoryStatus, PoiItem


# Mock POI 数据：所有 category 和 tags 都使用 Enum，避免 Agent 传入或读取不存在的值。
MOCK_POIS: List[PoiItem] = [
    PoiItem(
        poi_id="poi_science_kids_001",
        name="儿童科学馆",
        category=POICategory.ENTERTAINMENT,
        address="上海市黄浦区人民大道 200 号",
        location=Coordinate(lat=31.2297, lng=121.4752),
        tags=[POITag.KIDS_FRIENDLY, POITag.AGE_5_PLUS, POITag.EXHIBITION],
        rating=4.8,
        avg_price=88,
        opening_hours="09:30-17:30",
        description="适合 3-8 岁儿童的互动科学展馆，包含光影实验、机械搭建和亲子工作坊。",
    ),
    PoiItem(
        poi_id="poi_restaurant_light_001",
        name="轻食餐厅",
        category=POICategory.DINING,
        address="上海市静安区铜仁路 88 号",
        location=Coordinate(lat=31.2269, lng=121.4598),
        tags=[POITag.LOW_FAT, POITag.KIDS_FRIENDLY],
        rating=4.6,
        avg_price=72,
        opening_hours="10:00-21:00",
        description="主打低脂健康轻食、儿童小份套餐和高蛋白餐盘，适合健康饮食约束场景。",
    ),
    PoiItem(
        poi_id="poi_citywalk_001",
        name="梧桐城市漫游路线",
        category=POICategory.ENTERTAINMENT,
        address="上海市徐汇区衡山路 900 号",
        location=Coordinate(lat=31.2048, lng=121.4436),
        tags=[POITag.CITY_WALK, POITag.KIDS_FRIENDLY, POITag.AGE_5_PLUS],
        rating=4.5,
        avg_price=0,
        opening_hours="06:00-22:00",
        description="适合家庭轻松散步的城市漫游路线，包含梧桐街区和儿童友好的休息点。",
    ),
    PoiItem(
        poi_id="poi_restaurant_family_002",
        name="小番茄家庭意面馆",
        category=POICategory.DINING,
        address="上海市黄浦区淮海中路 300 号",
        location=Coordinate(lat=31.2222, lng=121.4729),
        tags=[POITag.KIDS_FRIENDLY, POITag.GROUP_FRIENDLY],
        rating=4.4,
        avg_price=96,
        opening_hours="11:00-22:00",
        description="提供儿童座椅和不辣儿童餐，适合科学馆之后衔接晚餐。",
    ),
    PoiItem(
        poi_id="poi_retail_family_001",
        name="家庭生活精选店",
        category=POICategory.RETAIL,
        address="上海市静安区愚园路 520 号",
        location=Coordinate(lat=31.2243, lng=121.4474),
        tags=[POITag.KIDS_FRIENDLY, POITag.GROUP_FRIENDLY],
        rating=4.7,
        avg_price=128,
        opening_hours="10:30-20:00",
        description="提供亲子生活用品、轻户外装备和小型聚会补给，适合作为行程中的零售补充点。",
    ),
]


# Mock 库存/排队状态：以 poi_id 为主键，模拟来自库存中心、餐厅排队系统或票务系统的数据。
# remaining_capacity 可以代表剩余票量、可预约座位或可接待人数；不同 category 下含义略有差异，
# 但对 Agent 来说统一解释为“还能不能接待 party_size 人”。
MOCK_INVENTORY: Dict[str, InventoryStatus] = {
    "poi_science_kids_001": InventoryStatus(
        poi_id="poi_science_kids_001",
        is_bookable=True,
        current_queue_length=3,
        estimated_wait_time=12,
        remaining_capacity=36,
        updated_at=datetime.utcnow().isoformat(),
    ),
    "poi_restaurant_light_001": InventoryStatus(
        poi_id="poi_restaurant_light_001",
        is_bookable=True,
        current_queue_length=1,
        estimated_wait_time=8,
        remaining_capacity=18,
        updated_at=datetime.utcnow().isoformat(),
    ),
    "poi_citywalk_001": InventoryStatus(
        poi_id="poi_citywalk_001",
        is_bookable=True,
        current_queue_length=0,
        estimated_wait_time=0,
        remaining_capacity=999,
        updated_at=datetime.utcnow().isoformat(),
    ),
    "poi_restaurant_family_002": InventoryStatus(
        poi_id="poi_restaurant_family_002",
        is_bookable=False,
        current_queue_length=14,
        estimated_wait_time=55,
        remaining_capacity=0,
        updated_at=datetime.utcnow().isoformat(),
    ),
    "poi_retail_family_001": InventoryStatus(
        poi_id="poi_retail_family_001",
        is_bookable=True,
        current_queue_length=0,
        estimated_wait_time=0,
        remaining_capacity=6,
        updated_at=datetime.utcnow().isoformat(),
    ),
}


def get_poi_or_404(poi_id: str) -> PoiItem:
    """根据 poi_id 获取 POI；不存在时抛出统一业务错误。"""

    for poi in MOCK_POIS:
        if poi.poi_id == poi_id:
            return poi
    raise HTTPException(status_code=404, detail=f"POI 不存在: {poi_id}")
