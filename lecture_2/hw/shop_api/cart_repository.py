from typing import List

from lecture_2.hw.shop_api.model import Cart


class CartRepository:
    __carts__: dict[int, Cart] = dict()
    __id__ = 0

    def create_cart(self) -> int:
        cart = Cart(self.__id__, [], 0)
        self.__carts__[cart.id] = cart
        self.__id__ += 1
        return cart.id

    def get_cart(self, id: int) -> Cart | None:
        return self.__carts__.get(id)

    def get_carts(self,
                  offset: int = 0,
                  limit: int = 0,
                  min_price: float | None = None,
                  max_price: float | None = None,
                  min_quantity: int | None = None,
                  max_quantity: int | None = None) -> List[Cart]:
        carts = list(self.__carts__.values())

        # Применение фильтрации по цене
        if min_price is not None:
            carts = [cart for cart in carts if cart.price >= min_price]
        if max_price is not None:
            carts = [cart for cart in carts if cart.price <= max_price]

        # Фильтрация по количеству товаров
        if min_quantity is not None:
            carts = [cart for cart in carts if len(cart.items) >= min_quantity]
        if max_quantity is not None:
            carts = [cart for cart in carts if len(cart.items) <= max_quantity]

        total_carts = len(carts)
        if offset >= total_carts:
            return []  # Если смещение больше, чем количество корзин, вернуть пустой список

        # Ограничение с учетом того, что limit может выходить за пределы списка
        end_index = min(offset + limit, total_carts)

        # Применение смещения и ограничения
        return carts[offset:end_index]