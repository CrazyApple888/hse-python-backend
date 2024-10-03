from lecture_2.hw.shop_api.model import Item


class ItemRepository:
    __items__: dict[int, Item] = dict()
    __id__ = 0

    def add_item(self, name: str, price: float) -> Item:
        item = Item(
            id=self.__id__,
            name=name,
            price=price,
            deleted=False
        )
        self.__id__ += 1
        self.__items__[item.id] = item

        return item

    def get_item(self, id: int) -> Item | None:
        item = self.__items__.get(id)
        if item.deleted:
            return None
        else:
            return item

    def update_item(self, id: int, name: str | None, price: float | None) -> Item | None:
        item = self.__items__.get(id)
        if item is None or item.deleted:
            return None
        if name is not None:
            item.name = name
        if price is not None:
            item.price = price
        self.__items__[id] = item

        return item

    def delete_item(self, id):
        item = self.__items__.get(id)
        if item is None:
            return
        item.deleted = True
