from typing import List

from lecture_2.hw.shop_api.model import Item


class ItemRepository:
    __items: dict[int, Item] = dict()
    __id = 0

    def add_item(self, name: str, price: float) -> Item:
        item = Item(
            id=self.__id,
            name=name,
            price=price,
            deleted=False
        )
        self.__id += 1
        self.__items[item.id] = item

        return item

    def get_item(self, id: int) -> Item | None:
        item = self.__items.get(id)
        if item.deleted:
            return None
        else:
            return item

    def update_item(self, id: int, name: str | None, price: float | None) -> Item | None:
        item = self.__items.get(id)
        if item is None or item.deleted:
            return None
        if name is not None:
            item.name = name
        if price is not None:
            item.price = price
        self.__items[id] = item

        return item

    def delete_item(self, id):
        item = self.__items.get(id)
        if item is None:
            return
        item.deleted = True

    def get_items(self,
                  offset: int,
                  limit: int,
                  min_price: float | None,
                  max_price: float | None,
                  show_deleted: bool) -> List[Item]:

        items = list(self.__items.values())

        if not show_deleted:
            items = [item for item in items if not item.deleted]

        if min_price is not None:
            items = [item for item in items if item.price >= min_price]
        if max_price is not None:
            items = [item for item in items if item.price <= max_price]

        total_items = len(items)
        if offset >= total_items:
            return []

        end_index = min(offset + limit, total_items)

        return items[offset:end_index]
