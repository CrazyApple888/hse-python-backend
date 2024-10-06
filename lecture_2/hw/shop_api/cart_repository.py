from typing import List

from lecture_2.hw.shop_api.model import Cart, Item


class CartRepository:
    __carts: dict[int, Cart] = dict()
    __id = 0

    def create_cart(self) -> int:
        cart = Cart(self.__id, [], 0)
        self.__carts[cart.id] = cart
        self.__id += 1
        return cart.id

    def get_cart(self, id: int) -> Cart | None:
        return self.__carts.get(id)

    def get_carts(self,
                  offset: int = 0,
                  limit: int = 0,
                  min_price: float | None = None,
                  max_price: float | None = None,
                  min_quantity: int | None = None,
                  max_quantity: int | None = None) -> List[Cart]:
        carts = list(self.__carts.values())

        if min_price is not None:
            carts = [cart for cart in carts if cart.price >= min_price]
        if max_price is not None:
            carts = [cart for cart in carts if cart.price <= max_price]

        if min_quantity is not None:
            carts = [cart for cart in carts if len(cart.items) >= min_quantity]
        if max_quantity is not None:
            carts = [cart for cart in carts if len(cart.items) <= max_quantity]

        total_carts = len(carts)
        if offset >= total_carts:
            return []

        end_index = min(offset + limit, total_carts)

        return carts[offset:end_index]

    def add_item(self, cart_id: int, item: Item) -> Cart | None:
        cart = self.__carts.get(cart_id)
        if cart is None:
            return None
        cart.items.append(item)
        cart.price += item.price

        return cart
