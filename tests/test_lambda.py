
import json
from src.lambda_function import lambda_handler


def invoke(method, path, body=None):
    event = {
        "requestContext": {
            "http": {"method": method}
        },
        "rawPath": path,
    }

    if body is not None:
        event["body"] = json.dumps(body)

    return lambda_handler(event, None)


def test_health():
    result = invoke("GET", "/health")
    assert result["statusCode"] == 200
    assert json.loads(result["body"])["status"] == "healthy"


def test_get_orders():
    result = invoke("GET", "/orders")
    assert result["statusCode"] == 200
    assert len(json.loads(result["body"])["orders"]) == 2


def test_create_order():
    result = invoke("POST", "/orders", {"item": "Laptop"})
    assert result["statusCode"] == 201
    body = json.loads(result["body"])
    assert body["item"] == "Laptop"
    assert body["order_id"]


def test_missing_item():
    result = invoke("POST", "/orders", {})
    assert result["statusCode"] == 400


def test_unknown_route():
    result = invoke("GET", "/invalid")
    assert result["statusCode"] == 404
