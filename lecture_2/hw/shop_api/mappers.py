from lecture_2.hw.shop_api.dto import CartDto, ItemDto
from lecture_2.hw.shop_api.model import Cart, Item


def cart_to_cart_dto(cart: Cart) -> CartDto:
    return CartDto(
        id=cart.id,
        items=list(map(item_to_item_dto, cart.items)),
        price=cart.price,
    )


def item_to_item_dto(item: Item) -> ItemDto:
    return ItemDto(
        id=item.id,
        name=item.name,
        price=item.price,
        deleted=item.deleted,
    )


def item_dto_to_item(item_dto: ItemDto) -> Item:
    return Item(
        id=item_dto.id,
        name=item_dto.name,
        price=item_dto.price,
        deleted=item_dto.deleted,
    )
