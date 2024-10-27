from http import HTTPStatus

import pytest

from tests.accesor import TestAccessor

from srv.schemas.base import DishResponse


URL = "dishes"


pytestmark = pytest.mark.asyncio


async def test_create_update_dish(test_accessor: TestAccessor, data_for_create_dish: dict):
    resp = await test_accessor.client.post(
        f"{test_accessor.ctx.path_v1}/{URL}", json=data_for_create_dish
    )
    assert resp.status == HTTPStatus.OK
    assert await test_accessor.db.check_record_exist(
        test_accessor.conn, test_accessor.db.dishes, data_for_create_dish
    )


async def test_get_dishes(test_accessor: TestAccessor, create_dish: dict):
    resp = await test_accessor.client.get(f"{test_accessor.ctx.path_v1}/{URL}")
    assert resp.status == HTTPStatus.OK
    assert DishResponse().validate(await resp.json(), many=True) == {}


async def test_get_dishes_not_exists(test_accessor: TestAccessor):
    resp = await test_accessor.client.get(f"{test_accessor.ctx.path_v1}/{URL}")
    assert resp.status == HTTPStatus.NO_CONTENT


async def test_delete_dish_by_id(test_accessor: TestAccessor, create_dish: dict):
    resp = await test_accessor.client.delete(
        f"{test_accessor.ctx.path_v1}/{URL}", params={"id": create_dish["id"]}
    )
    assert resp.status == HTTPStatus.OK
    assert not await test_accessor.db.check_record_exist(
        test_accessor.conn, test_accessor.db.dishes, create_dish
    )


async def test_delete_dish_by_name(test_accessor: TestAccessor, create_dish: dict):
    resp = await test_accessor.client.delete(
        f"{test_accessor.ctx.path_v1}/{URL}", params={"name": create_dish["name"]}
    )
    assert resp.status == HTTPStatus.OK
    assert not await test_accessor.db.check_record_exist(
        test_accessor.conn, test_accessor.db.dishes, create_dish
    )