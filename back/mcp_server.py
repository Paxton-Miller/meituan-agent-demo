from __future__ import annotations

import argparse
from typing import Any, Dict, Optional

from back.agent_tools.registry import registry


def create_mcp_server(
    host: str = "127.0.0.1",
    port: int = 8001,
    sse_path: str = "/sse",
    message_path: str = "/messages/",
    streamable_http_path: str = "/mcp",
):
    """Create an MCP server that exposes the same registry used by REST/OpenAI adapters."""

    try:
        from mcp.server.fastmcp import FastMCP
    except ImportError as exc:
        raise RuntimeError("请先安装 mcp 包才能启动 MCP Server。") from exc

    mcp = FastMCP(
        "meituan-agent-tools",
        host=host,
        port=port,
        sse_path=sse_path,
        message_path=message_path,
        streamable_http_path=streamable_http_path,
    )

    @mcp.tool()
    async def get_user_context() -> Dict[str, Any]:
        """获取当前用户位置、家庭地址和基础偏好画像。"""

        return await registry.invoke("get_user_context", {})

    @mcp.tool()
    async def estimate_route(
        origin_lat: float,
        origin_lng: float,
        dest_lat: float,
        dest_lng: float,
        travel_mode: str = "TAXI",
    ) -> Dict[str, Any]:
        """估算两个坐标点之间的路线距离和出行耗时。"""

        return await registry.invoke(
            "estimate_route",
            {
                "origin_lat": origin_lat,
                "origin_lng": origin_lng,
                "dest_lat": dest_lat,
                "dest_lng": dest_lng,
                "travel_mode": travel_mode,
            },
        )

    @mcp.tool()
    async def search_pois(
        location: Optional[str] = None,
        radius: int = 5000,
        category: Optional[str] = None,
        tags: Optional[list[str]] = None,
    ) -> Dict[str, Any]:
        """根据位置、业态分类和语义标签搜索本地生活 POI 候选。"""

        return await registry.invoke(
            "search_pois",
            {
                "location": location,
                "radius": radius,
                "category": category,
                "tags": tags,
            },
        )

    @mcp.tool()
    async def get_poi_status(
        poi_id: str,
        party_size: int,
        target_time: Optional[str] = None,
    ) -> Dict[str, Any]:
        """查询 POI 的实时可预订状态、剩余容量、排队长度和等待时间。"""

        return await registry.invoke(
            "get_poi_status",
            {
                "poi_id": poi_id,
                "party_size": party_size,
                "target_time": target_time,
            },
        )

    @mcp.tool()
    async def reserve_booking(
        poi_id: str,
        party_size: int,
        reserve_time: str,
        idempotency_key: Optional[str] = None,
    ) -> Dict[str, Any]:
        """在用户确认后创建 POI 预订订单，并扣减 mock 库存。"""

        return await registry.invoke(
            "reserve_booking",
            {
                "poi_id": poi_id,
                "party_size": party_size,
                "reserve_time": reserve_time,
                "idempotency_key": idempotency_key,
            },
        )

    return mcp


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Meituan Agent MCP server.")
    parser.add_argument(
        "--transport",
        choices=["stdio", "sse", "streamable-http"],
        default="stdio",
        help="MCP transport. Use stdio for local clients, sse/streamable-http for remote clients.",
    )
    parser.add_argument("--host", default="127.0.0.1", help="Host for HTTP-based transports.")
    parser.add_argument("--port", type=int, default=8001, help="Port for HTTP-based transports.")
    parser.add_argument("--sse-path", default="/sse", help="SSE endpoint path.")
    parser.add_argument("--message-path", default="/messages/", help="SSE message endpoint path.")
    parser.add_argument(
        "--streamable-http-path",
        default="/mcp",
        help="Streamable HTTP endpoint path.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    server = create_mcp_server(
        host=args.host,
        port=args.port,
        sse_path=args.sse_path,
        message_path=args.message_path,
        streamable_http_path=args.streamable_http_path,
    )
    server.run(transport=args.transport)
