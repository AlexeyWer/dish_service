from http import HTTPStatus

import pytest

from tests.accesor import TestAccessor


pytestmark = pytest.mark.asyncio


async def test_liveness(test_accessor: TestAccessor):
    resp = await test_accessor.client.get(f"{test_accessor.ctx.path_v1}/liveness")
    assert resp.status == HTTPStatus.OK


async def test_readiness(test_accessor: TestAccessor):
    resp = await test_accessor.client.get(f"{test_accessor.ctx.path_v1}/readiness")
    assert resp.status == HTTPStatus.OK

async def test_docs(test_accessor: TestAccessor):
    resp = await test_accessor.client.get(f"{test_accessor.ctx.config.name}/docs")
    assert resp.status == HTTPStatus.OK