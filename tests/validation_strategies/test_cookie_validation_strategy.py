import simplejson as json
import pytest

from gemstone.auth.validation_strategies import BasicCookieStrategy

from tests.services.service_validation_strategies import ValidationStrategyTestService

VS_COOKIE = BasicCookieStrategy("authToken")


@pytest.fixture
def app():
    service = ValidationStrategyTestService()
    service.set_validation_strategy(VS_COOKIE)
    return service.make_tornado_app()


@pytest.mark.gen_test
def test_cookie_strategy_token_wrong(http_client, base_url):
    base_url += "/api"
    body = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "private_echo",
        "params": ["test"]
    }
    result = yield http_client.fetch(base_url, method="POST", body=json.dumps(body),
                                     headers={"content-type": "application/json",
                                              "cookie": "authCookie=wrong_token"})
    assert result.code == 200
    result_body = json.loads(result.body)
    print(result_body)
    assert result_body["id"] == 1
    assert result_body["result"] is None
    assert result_body["error"] is not None
    assert result_body["error"]["code"] == -32001
    assert result_body["error"]["message"] == "Access denied"


@pytest.mark.gen_test
def test_cookie_strategy_token_ok(http_client, base_url):
    base_url += "/api"
    body = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "private_echo",
        "params": ["test"]
    }
    result = yield http_client.fetch(base_url, method="POST", body=json.dumps(body),
                                     headers={"content-type": "application/json",
                                              "cookie": "authToken=secret"})
    assert result.code == 200
    result_body = json.loads(result.body)
    print(result_body)
    assert result_body["id"] == 1
    assert result_body["result"] == "test"
    assert result_body["error"] is None


@pytest.mark.gen_test
def test_cookie_strategy_token_ok_wrong_cookie_name(http_client, base_url):
    base_url += "/api"
    body = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "private_echo",
        "params": ["test"]
    }
    result = yield http_client.fetch(base_url, method="POST", body=json.dumps(body),
                                     headers={"content-type": "application/json",
                                              "cookie": "authTokenWrong=secret"})
    assert result.code == 200
    result_body = json.loads(result.body)
    print(result_body)
    assert result_body["id"] == 1
    assert result_body["result"] is None
    assert result_body["error"] is not None
    assert result_body["error"]["code"] == -32001
    assert result_body["error"]["message"] == "Access denied"


@pytest.mark.gen_test
def test_cookie_strategy_notification_token_wrong(http_client, base_url):
    base_url += "/api"
    body = {
        "jsonrpc": "2.0",
        "method": "private_echo",
        "params": ["test"]
    }
    result = yield http_client.fetch(base_url, method="POST", body=json.dumps(body),
                                     headers={"content-type": "application/json",
                                              "cookie": "authToken=wrong_token"})
    assert result.code == 200
    result_body = json.loads(result.body)
    print(result_body)
    assert "id" not in result_body
    assert result_body["result"] is None
    assert result_body["error"] is None


@pytest.mark.gen_test
def test_cookie_strategy_notification_token_ok(http_client, base_url):
    base_url += "/api"
    body = {
        "jsonrpc": "2.0",
        "method": "private_echo",
        "params": ["test"]
    }
    result = yield http_client.fetch(base_url, method="POST", body=json.dumps(body),
                                     headers={"content-type": "application/json",
                                              "cookie": "authToken=secret"})
    assert result.code == 200
    result_body = json.loads(result.body)
    print(result_body)
    assert "id" not in result_body
    assert result_body["result"] is None
    assert result_body["error"] is None
