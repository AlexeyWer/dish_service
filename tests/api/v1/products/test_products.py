from http import HTTPStatus

import pytest

from tests.accesor import TestAccessor

from srv.schemas.base import ProductResponse


URL = "products"


pytestmark = pytest.mark.asyncio


async def test_create_update_product(test_accessor: TestAccessor, data_for_create_product: dict):
    resp = await test_accessor.client.post(
        f"{test_accessor.ctx.path_v1}/{URL}", json=data_for_create_product
    )
    assert resp.status == HTTPStatus.OK
    assert await test_accessor.db.check_record_exist(
        test_accessor.conn, test_accessor.db.products, data_for_create_product
    )


async def test_get_products(test_accessor: TestAccessor, create_product: dict):
    resp = await test_accessor.client.get(f"{test_accessor.ctx.path_v1}/{URL}")
    assert resp.status == HTTPStatus.OK
    assert ProductResponse().validate(await resp.json(), many=True) == {}


async def test_get_products_not_exists(test_accessor: TestAccessor):
    resp = await test_accessor.client.get(f"{test_accessor.ctx.path_v1}/{URL}")
    assert resp.status == HTTPStatus.NO_CONTENT


async def test_delete_product_by_id(test_accessor: TestAccessor, create_product: dict):
    resp = await test_accessor.client.delete(
        f"{test_accessor.ctx.path_v1}/{URL}", params={"id": create_product["id"]}
    )
    assert resp.status == HTTPStatus.OK
    assert not await test_accessor.db.check_record_exist(
        test_accessor.conn, test_accessor.db.products, create_product
    )


async def test_delete_products_by_name(test_accessor: TestAccessor, create_product: dict):
    resp = await test_accessor.client.delete(
        f"{test_accessor.ctx.path_v1}/{URL}", params={"name": create_product["name"]}
    )
    assert resp.status == HTTPStatus.OK
    assert not await test_accessor.db.check_record_exist(
        test_accessor.conn, test_accessor.db.products, create_product
    )