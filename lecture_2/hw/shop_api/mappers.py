from collections import defaultdict

from lecture_2.hw.shop_api.dto import CartDto, ItemDto
from lecture_2.hw.shop_api.model import Cart, Item


def cart_to_cart_dto(cart: Cart) -> CartDto:
    item_quantities = defaultdict(lambda: {'item': None, 'quantity': 0})

    for item in cart.items:
        if item_quantities[item.id]['item'] is None:
            item_quantities[item.id]['item'] = item
        item_quantities[item.id]['quantity'] += 1

    unique_items = [
        item_to_item_dto(item_data['item'], item_data['quantity'])
        for item_data in item_quantities.values()
    ]

    return CartDto(
        id=cart.id,
        items=unique_items,
        price=cart.price,
    )


def item_to_item_dto(item: Item, quantity: int = 1) -> ItemDto:
    return ItemDto(
        id=item.id,
        name=item.name,
        price=item.price,
        deleted=item.deleted,
        quantity=quantity,
    )


def item_dto_to_item(item_dto: ItemDto) -> Item:
    return Item(
        id=item_dto.id,
        name=item_dto.name,
        price=item_dto.price,
        deleted=item_dto.deleted,
    )
