from http import HTTPStatus

import pytest

from tests.accesor import TestAccessor

from srv.schemas.base import ProductInDishResponse


pytestmark = pytest.mark.asyncio


def get_url_by_dish_id(dish_id: int) -> str:
    return f"dish/{dish_id}/products"


async def test_create_update_product_in_dish(test_accessor: TestAccessor, data_for_create_product_in_dish: dict):
    posftix_url = get_url_by_dish_id(data_for_create_product_in_dish["dish"])
    resp = await test_accessor.client.post(
        f"{test_accessor.ctx.path_v1}/{posftix_url}", json=data_for_create_product_in_dish
    )
    assert resp.status == HTTPStatus.OK
    assert await test_accessor.db.check_record_exist(
        test_accessor.conn, test_accessor.db.products_in_dishes, data_for_create_product_in_dish
    )


async def test_get_products_in_dish(test_accessor: TestAccessor, create_product_in_dish: dict):
    posftix_url = get_url_by_dish_id(create_product_in_dish["dish"])
    resp = await test_accessor.client.get(f"{test_accessor.ctx.path_v1}/{posftix_url}")
    assert resp.status == HTTPStatus.OK
    assert ProductInDishResponse().validate(await resp.json(), many=True) == {}


async def test_get_products_in_dish_not_exists(test_accessor: TestAccessor):
    resp = await test_accessor.client.get(f"{test_accessor.ctx.path_v1}/{get_url_by_dish_id(1)}",)
    assert resp.status == HTTPStatus.NO_CONTENT


async def test_delete_product_in_dish(test_accessor: TestAccessor, create_product_in_dish: dict):
    posftix_url = get_url_by_dish_id(create_product_in_dish["dish"])
    resp = await test_accessor.client.delete(
        f"{test_accessor.ctx.path_v1}/{posftix_url}", params={"id": create_product_in_dish["id"]}
    )
    assert resp.status == HTTPStatus.OK
    assert not await test_accessor.db.check_record_exist(
        test_accessor.conn, test_accessor.db.products_in_dishes, create_product_in_dish
    )
