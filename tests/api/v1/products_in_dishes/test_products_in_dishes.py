from http import HTTPStatus

import pytest

from tests.accesor import TestAccessor

from srv.schemas.base import ProductInDishResponse


URL = "dishes/products"


pytestmark = pytest.mark.asyncio


async def test_create_update_product_in_dish(test_accessor: TestAccessor, data_for_create_product_in_dish: dict):
    resp = await test_accessor.client.post(
        f"{test_accessor.ctx.path_v1}/{URL}", json=data_for_create_product_in_dish
    )
    assert resp.status == HTTPStatus.OK
    assert await test_accessor.db.check_record_exist(
        test_accessor.conn, test_accessor.db.products_in_dishes, data_for_create_product_in_dish
    )


async def test_get_products_in_dish(test_accessor: TestAccessor, create_product_in_dish: dict):
    resp = await test_accessor.client.get(
        f"{test_accessor.ctx.path_v1}/{URL}", params={"id": create_product_in_dish["dish"]}
        )
    assert resp.status == HTTPStatus.OK
    assert ProductInDishResponse().validate(await resp.json(), many=True) == {}


async def test_get_products_in_dish_not_exists(test_accessor: TestAccessor):
    resp = await test_accessor.client.get(f"{test_accessor.ctx.path_v1}/{URL}", params={"id": 0})
    assert resp.status == HTTPStatus.NO_CONTENT


async def test_delete_product_in_dish(test_accessor: TestAccessor, create_product_in_dish: dict):
    resp = await test_accessor.client.delete(
        f"{test_accessor.ctx.path_v1}/{URL}", params={"id": create_product_in_dish["id"]}
    )
    assert resp.status == HTTPStatus.OK
    assert not await test_accessor.db.check_record_exist(
        test_accessor.conn, test_accessor.db.products_in_dishes, create_product_in_dish
    )
