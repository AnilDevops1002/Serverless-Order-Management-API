import json
import os

os.environ["TELEMETRY_ENABLED"] = "false"

from src.lambda_function import lambda_handler


def make_event(method, path, body=None):
    event = {
        "version": "2.0",
        "routeKey": f"{method} {path}",
        "rawPath": path,
        "requestContext": {
            "http": {
                "method": method,
                "path": path,
            }
        },
        "isBase64Encoded": False,
    }

    if body is not None:
        event["body"] = json.dumps(body)

    return event


def test_health_endpoint():
    response = lambda_handler(make_event("GET", "/health"), None)
    assert response["statusCode"] == 200


def test_get_orders_endpoint():
    response = lambda_handler(make_event("GET", "/orders"), None)
    assert response["statusCode"] == 200
    assert isinstance(json.loads(response["body"]), (list, dict))


def test_create_order_endpoint():
    response = lambda_handler(
        make_event("POST", "/orders", {"item": "Laptop"}),
        None,
    )
    assert response["statusCode"] == 201


def test_invalid_order_endpoint():
    response = lambda_handler(
        make_event("POST", "/orders", {}),
        None,
    )
    assert response["statusCode"] == 400


def test_unknown_endpoint():
    response = lambda_handler(
        make_event("GET", "/invalid"),
        None,
    )
    assert response["statusCode"] == 404
