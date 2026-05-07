from __future__ import annotations

import inspect
from dataclasses import dataclass, field
from typing import Any, Awaitable, Callable, Dict, Generic, List, Optional, Type, TypeVar

from pydantic import BaseModel, ValidationError

from back.services.errors import ServiceError


InputModel = TypeVar("InputModel", bound=BaseModel)
OutputModel = TypeVar("OutputModel", bound=BaseModel)


def model_to_dict(model: BaseModel) -> Dict[str, Any]:
    if hasattr(model, "model_dump"):
        return model.model_dump(mode="json")  # type: ignore[attr-defined]
    return model.dict()


def model_to_schema(model_class: Type[BaseModel]) -> Dict[str, Any]:
    if hasattr(model_class, "model_json_schema"):
        return model_class.model_json_schema()  # type: ignore[attr-defined]
    return model_class.schema()


def validate_model(model_class: Type[InputModel], payload: Dict[str, Any]) -> InputModel:
    if hasattr(model_class, "model_validate"):
        return model_class.model_validate(payload)  # type: ignore[attr-defined]
    return model_class.parse_obj(payload)


@dataclass(frozen=True)
class ToolExecutionContext:
    request_id: Optional[str] = None
    actor: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class AgentTool(Generic[InputModel, OutputModel]):
    name: str
    description: str
    input_model: Type[InputModel]
    output_model: Type[OutputModel]
    handler: Callable[[InputModel, ToolExecutionContext], Awaitable[OutputModel] | OutputModel]
    side_effect: bool = False
    tags: List[str] = field(default_factory=list)
    timeout_seconds: float = 10.0
    idempotent: bool = True

    @property
    def input_schema(self) -> Dict[str, Any]:
        schema = model_to_schema(self.input_model)
        schema.setdefault("additionalProperties", False)
        return schema

    @property
    def output_schema(self) -> Dict[str, Any]:
        return model_to_schema(self.output_model)

    async def invoke(
        self,
        arguments: Dict[str, Any],
        context: Optional[ToolExecutionContext] = None,
    ) -> Dict[str, Any]:
        try:
            typed_arguments = validate_model(self.input_model, arguments)
            result = self.handler(typed_arguments, context or ToolExecutionContext())
            if inspect.isawaitable(result):
                result = await result
            return model_to_dict(result)
        except ValidationError as exc:
            raise ServiceError(status_code=422, message=f"工具 {self.name} 入参校验失败: {exc}") from exc
        except ServiceError:
            raise
        except Exception as exc:
            raise ServiceError(status_code=500, message=f"工具 {self.name} 执行失败: {exc}") from exc

    def manifest(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "input_schema": self.input_schema,
            "output_schema": self.output_schema,
            "side_effect": self.side_effect,
            "idempotent": self.idempotent,
            "timeout_seconds": self.timeout_seconds,
            "tags": self.tags,
        }
