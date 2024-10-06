from typing import List, Annotated

from fastapi import FastAPI, HTTPException
from fastapi.params import Query
from starlette import status
from starlette.responses import Response

from lecture_2.hw.shop_api.cart_repository import CartRepository
from lecture_2.hw.shop_api.dto import CartDto, ItemDto, CreateItemRequest, PutItemRequest, PatchItemRequest
from lecture_2.hw.shop_api.item_repository import ItemRepository
from lecture_2.hw.shop_api.mappers import cart_to_cart_dto, item_to_item_dto

app = FastAPI(title="Shop API")
item_repository = ItemRepository()
cart_repository = CartRepository()


@app.post(
    path="/cart",
    status_code=status.HTTP_201_CREATED,
)
def create_cart(response: Response):
    card_id = cart_repository.create_cart()
    response.headers['location'] = f'/cart/{card_id}'
    return {"id": card_id}


@app.get(
    path="/cart/{id}"
)
def get_card(id: int) -> CartDto:
    cart = cart_repository.get_cart(id)
    if cart is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    return cart_to_cart_dto(cart)


@app.get(
    path="/cart"
)
def get_carts(offset: Annotated[int, Query(ge=0)] = 0,
              limit: Annotated[int, Query(gt=0)] = 10,
              min_price: Annotated[float | None, Query(gt=0)] = None,
              max_price: Annotated[float | None, Query(gt=0)] = None,
              min_quantity: Annotated[int | None, Query(ge=0)] = None,
              max_quantity: Annotated[int | None, Query(ge=0)] = None) -> List[CartDto]:
    carts = cart_repository.get_carts(offset, limit, min_price, max_price, min_quantity, max_quantity)
    return list(map(cart_to_cart_dto, carts))

@app.post(
    path="/cart/{cart_id}/add/{item_id}"
)
def add_item_to_cart(cart_id: int, item_id: int) -> CartDto:
    item = item_repository.get_item(item_id)
    if item is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    cart = cart_repository.add_item(cart_id, item)
    if cart is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return cart_to_cart_dto(cart)

@app.post(
    path="/item",
    status_code=status.HTTP_201_CREATED,
)
def add_item(item: CreateItemRequest) -> ItemDto:
    return item_to_item_dto(item_repository.add_item(item.name, item.price))


@app.get(
    path="/item/{id}"
)
def get_item(id: int) -> ItemDto:
    item = item_repository.get_item(id)
    if item is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    return item_to_item_dto(item)


@app.get(
    path="/item"
)
def get_items(offset: int = 0,
              limit: int = 0,
              min_price: float | None = None,
              max_price: float | None = None,
              show_deleted: bool = False):
    ...


@app.put(
    path="/item/{id}"
)
def put_item(id: int, request: PutItemRequest):
    item = item_repository.update_item(id, request.name, request.price)
    if item is None:
        raise HTTPException(status.HTTP_304_NOT_MODIFIED)
    return item_to_item_dto(item)


@app.patch(
    path="/item/{id}"
)
def patch_item(id: int, request: PatchItemRequest):
    item = item_repository.update_item(id, request.name, request.price)
    if item is None:
        raise HTTPException(status.HTTP_304_NOT_MODIFIED)

    return item_to_item_dto(item)


@app.delete(
    path="/item/{id}"
)
def delete_item(id: int):
    item_repository.delete_item(id)
