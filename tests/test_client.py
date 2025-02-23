import pytest

from sanic.app import Sanic
from sanic import response


async def test_fixture_sanic_client_get_properties(test_cli):
    assert test_cli.app is not None
    assert test_cli.host is not None
    assert test_cli.port is not None
    assert test_cli.server is not None
    assert test_cli.session is not None


async def test_fixture_sanic_client_make_url(test_cli):
    uri = '/test'
    url = test_cli.make_url(uri)
    assert url == "http://127.0.0.1:{port}/test".format(port=str(test_cli.port))


async def test_fixture_sanic_client_get(test_cli):
    resp = await test_cli.get('/test_get')
    assert resp.status_code == 200
    resp_json = resp.json()
    assert resp_json == {"GET": True}


async def test_fixture_sanic_client_post(test_cli):
    resp = await test_cli.post('/test_post')
    assert resp.status_code == 200
    resp_json = resp.json()
    assert resp_json == {"POST": True}


async def test_fixture_sanic_client_put(test_cli):
    resp = await test_cli.put('/test_put')
    assert resp.status_code == 200
    resp_json = resp.json()
    assert resp_json == {"PUT": True}


async def test_fixture_sanic_client_delete(test_cli):
    resp = await test_cli.delete('/test_delete')
    assert resp.status_code == 200
    resp_json = resp.json()
    assert resp_json == {"DELETE": True}


async def test_fixture_sanic_client_patch(test_cli):
    resp = await test_cli.patch('/test_patch')
    assert resp.status_code == 200
    resp_json = resp.json()
    assert resp_json == {"PATCH": True}


async def test_fixture_sanic_client_options(test_cli):
    resp = await test_cli.options('/test_options')
    assert resp.status_code == 200
    resp_json = resp.json()
    assert resp_json == {"OPTIONS": True}


async def test_fixture_sanic_client_head(test_cli):
    resp = await test_cli.head('/test_head')
    assert resp.status_code == 200
    # HEAD should not have body
    assert resp.content == b""


async def test_fixture_sanic_client_blueprint_get(test_cli):
    resp = await test_cli.get('/bp_group/bp_route/test_get')
    assert resp.status_code == 200
    resp_json = resp.json()
    assert resp_json == {"blueprint": "get"}


async def test_fixture_sanic_client_close(test_cli):
    resp = await test_cli.get('/test_get')
    assert resp.status_code == 200
    resp_json = resp.json()
    assert resp_json == {"GET": True}
    await test_cli.close()
    assert test_cli._closed == True


async def test_fixture_sanic_client_passing_headers(test_cli):
    headers={"authorization": "Basic bG9naW46cGFzcw=="}
    resp = await test_cli.get('/test_passing_headers', headers=headers)
    assert resp.status_code == 200
    resp_json = resp.json()
    assert resp_json["headers"]["authorization"] == headers["authorization"]


async def test_fixture_sanic_client_context_manager(app, sanic_client):
    async with await sanic_client(app) as test_cli:
        resp = await test_cli.get('/test_get')
        assert resp.status_code == 200
        resp_json = resp.json()
        assert resp_json == {"GET": True}


async def test_fixture_test_client_context_manager(app, test_client):
    async with await test_client(app) as test_cli:
        resp = await test_cli.get('/test_get')
        assert resp.status_code == 200
        resp_json = resp.json()
        assert resp_json == {"GET": True}


async def test_fixture_sanic_client_raise_exception_for_non_sanic_app(sanic_client):
    class SimpleApplication:
        pass
    with pytest.raises(TypeError):
        await sanic_client(SimpleApplication())

