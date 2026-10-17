import os
from flask import Flask, request, Response

from src.lambda_function import lambda_handler

app = Flask(__name__)


@app.route("/", defaults={"path": ""}, methods=["GET", "POST"])
@app.route("/<path:path>", methods=["GET", "POST"])
def handle_request(path):
    event = {
        "version": "2.0",
        "rawPath": request.path,
        "requestContext": {
            "http": {
                "method": request.method,
                "path": request.path,
            }
        },
        "body": request.get_data(as_text=True),
        "isBase64Encoded": False,
    }

    result = lambda_handler(event, None)

    return Response(
        response=result["body"],
        status=result["statusCode"],
        content_type="application/json",
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8080"))
    app.run(host="0.0.0.0", port=port)
