from dataclasses import dataclass

@dataclass
class Item:
    id: int
    name: str
    price: float
    deleted: bool

@dataclass
class Cart:
    id: int
    items: list[Item]
    price: float