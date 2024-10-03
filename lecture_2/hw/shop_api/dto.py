from dataclasses import dataclass

from pydantic import Extra, Field, BaseModel, ConfigDict, model_validator


class ForbidUnknownBase(BaseModel):
    model_config = ConfigDict(extra='forbid')


@dataclass
class CreateItemRequest:
    name: str
    price: float


@dataclass
class ItemDto:
    id: int
    name: str
    price: float
    deleted: bool


@dataclass
class CartDto:
    id: int
    items: list[ItemDto]
    price: float


@dataclass
class PutItemRequest:
    name: str
    price: float


@dataclass
class PatchItemRequest(ForbidUnknownBase):
    name: str | None = Field(None)
    price: float | None = Field(None)
