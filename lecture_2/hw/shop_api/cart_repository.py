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

