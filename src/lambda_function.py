
import json
import time
import uuid
import logging

from opentelemetry.trace import Status, StatusCode
from src.observability import tracer, record_request

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body),
    }


def lambda_handler(event, context):
    start = time.perf_counter()

    method = (
        event.get("requestContext", {})
        .get("http", {})
        .get("method", event.get("httpMethod", "GET"))
    )
    path = event.get("rawPath", event.get("path", "/"))

    with tracer.start_as_current_span("order-api-request") as span:
        span.set_attribute("http.request.method", method)
        span.set_attribute("url.path", path)

        try:
            if method == "GET" and path == "/health":
                result = response(200, {
                    "status": "healthy",
                    "service": "order-api",
                    "version": "v1",
                })

            elif method == "GET" and path == "/orders":
                result = response(200, {
                    "orders": [
                        {
                            "id": "1001",
                            "item": "Laptop",
                            "status": "created",
                        },
                        {
                            "id": "1002",
                            "item": "Mouse",
                            "status": "shipped",
                        },
                    ]
                })

            elif method == "POST" and path == "/orders":
                try:
                    body = json.loads(event.get("body") or "{}")

                    if not isinstance(body, dict) or not body.get("item"):
                        result = response(400, {
                            "error": "item is required"
                        })
                    else:
                        result = response(201, {
                            "order_id": str(uuid.uuid4()),
                            "item": body["item"],
                            "status": "created",
                        })

                except (json.JSONDecodeError, TypeError):
                    result = response(400, {
                        "error": "Invalid JSON"
                    })

            else:
                result = response(404, {
                    "error": "Route not found"
                })

        except Exception:
            logger.exception("Unexpected application error")
            span.set_status(Status(StatusCode.ERROR))
            result = response(500, {
                "error": "Internal server error"
            })

        duration_ms = round(
            (time.perf_counter() - start) * 1000, 2
        )
        status_code = result["statusCode"]

        span.set_attribute(
            "http.response.status_code", status_code
        )

        if status_code >= 500:
            span.set_status(Status(StatusCode.ERROR))

        record_request(
            method, path, status_code, duration_ms
        )

        logger.info(json.dumps({
            "event": "http_request",
            "method": method,
            "path": path,
            "status_code": status_code,
            "duration_ms": duration_ms,
        }))

        return result

