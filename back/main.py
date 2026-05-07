from __future__ import annotations

import time
from typing import Dict
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from back.api.routers import booking, poi, route, tools, user
from back.services.errors import ServiceError


app = FastAPI(
    title="本地生活活动规划与执行 Agent Mock API",
    description=(
        "面向大模型 Agent 调用的本地生活 Mock 服务，覆盖用户上下文、路线估算、"
        "POI 搜索、实时状态查询与预订交易执行。"
    ),
    version="1.0.0",
)


# CORS 配置：Mock 服务通常会被 Web UI、调试页面、Agent Sandbox 等不同来源调用，
# 因此这里允许所有来源、请求方法和请求头，降低本地联调成本。
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def request_context_middleware(request: Request, call_next):
    """Attach production-style tracing headers without changing API payloads."""

    request_id = request.headers.get("X-Request-ID", uuid4().hex)
    started_at = time.perf_counter()
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    elapsed_ms = round((time.perf_counter() - started_at) * 1000, 2)
    response.headers["X-Process-Time-Ms"] = str(elapsed_ms)
    return response


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_, exc: RequestValidationError) -> JSONResponse:
    """将 FastAPI/Pydantic 参数校验错误转换为统一 JSON 格式。"""

    return JSONResponse(
        status_code=422,
        content={"code": 422, "msg": f"请求参数校验失败: {exc.errors()}"},
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(_, exc: HTTPException) -> JSONResponse:
    """处理业务主动抛出的 HTTPException，保持 code/msg 结构一致。"""

    return JSONResponse(
        status_code=exc.status_code,
        content={"code": exc.status_code, "msg": str(exc.detail)},
    )


@app.exception_handler(ServiceError)
async def service_exception_handler(_, exc: ServiceError) -> JSONResponse:
    """Map domain errors consistently for REST callers and agent tool gateways."""

    return JSONResponse(
        status_code=exc.status_code,
        content={"code": exc.status_code, "msg": exc.message},
    )


@app.exception_handler(Exception)
async def global_exception_handler(_, exc: Exception) -> JSONResponse:
    """兜底异常处理，避免未捕获错误暴露堆栈信息给调用方。"""

    return JSONResponse(
        status_code=500,
        content={"code": 500, "msg": f"服务内部错误: {str(exc)}"},
    )


app.include_router(user.router)
app.include_router(route.router)
app.include_router(poi.router)
app.include_router(booking.router)
app.include_router(tools.router)


@app.get("/", summary="服务健康检查")
async def root() -> Dict[str, str]:
    """简单健康检查，方便浏览器直接访问确认服务已启动。"""

    return {"service": "meituan-agent-demo", "status": "ok"}
