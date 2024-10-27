import pytest_asyncio

from tests import get_data
from tests.accesor import TestAccessor


@pytest_asyncio.fixture
async def data_for_create_dish() -> dict:
    return get_data.get_dish_data()


@pytest_asyncio.fixture
async def create_dish(test_accessor: TestAccessor, data_for_create_dish: dict) -> dict:
    return await test_accessor.db.create_or_update_record(
        test_accessor.conn, data_for_create_dish, test_accessor.db.dishes
    )


@pytest_asyncio.fixture
async def data_for_create_product() -> dict:
    return get_data.get_product_data()


@pytest_asyncio.fixture
async def create_product(test_accessor: TestAccessor, data_for_create_product: dict) -> dict:
    return await test_accessor.db.create_or_update_record(
        test_accessor.conn, data_for_create_product, test_accessor.db.products
    )


@pytest_asyncio.fixture
async def data_for_create_product_in_dish(create_dish: dict, create_product: dict) -> dict:
    return get_data.get_product_in_dish_data(create_dish, create_product)


@pytest_asyncio.fixture
async def create_product_in_dish(test_accessor: TestAccessor, data_for_create_product_in_dish: dict) -> dict:
    return await test_accessor.db.create_or_update_record(
        test_accessor.conn, data_for_create_product_in_dish, test_accessor.db.products_in_dishes
    )
