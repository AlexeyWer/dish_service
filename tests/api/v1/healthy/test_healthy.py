from http import HTTPStatus

import pytest

from tests.app import TestApp


pytestmark = pytest.mark.asyncio


async def test_liveness(test_app: TestApp):
    resp = await test_app.client.get(f"{test_app.ctx.path_v1}/liveness")
    assert resp.status == HTTPStatus.OK


async def test_readiness(test_app: TestApp):
    resp = await test_app.client.get(f"{test_app.ctx.path_v1}/readiness")
    assert resp.status == HTTPStatus.OK

async def test_docs(test_app: TestApp):
    resp = await test_app.client.get(f"{test_app.ctx.config.name}/docs")
    assert resp.status == HTTPStatus.OK