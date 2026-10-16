
# Serverless Order Management API

Python-based Order Management API designed for AWS Lambda, with GitHub Actions CI and OpenTelemetry observability.

## Architecture

Client → HTTP API → AWS Lambda Order API

Application telemetry:
- Metrics → Grafana Cloud Prometheus
- Traces → Grafana Tempo
- Structured JSON logs → Application output

AWS deployment is pending account activation.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | /health | Returns application health |
| GET | /orders | Returns sample orders |
| POST | /orders | Creates a demonstration order |

Invalid requests return HTTP 400. Unknown routes return HTTP 404.

Orders are currently demonstration data and are not persisted.

## Technology Stack

- Python
- AWS Lambda handler
- OpenTelemetry
- Grafana Cloud
- GitHub Actions
- pytest

## Installation

Create a virtual environment:

    python3 -m venv .venv
    source .venv/bin/activate

Install dependencies:

    python -m pip install -r requirements-dev.txt

Run unit tests:

    TELEMETRY_ENABLED=false python -m pytest -v

## Observability

The application records:

- Request counts
- Server errors
- Request duration
- Distributed tracing spans
- Structured JSON request logs

Grafana dashboard:
DevOps Lambda - Application Observability

## GitHub Actions CI

The workflow runs on pushes and pull requests to main.

Steps:
1. Checkout source code
2. Set up Python 3.13
3. Install dependencies
4. Run five automated tests

## Security

- Secrets are stored outside source control.
- The .env file is ignored by Git.
- Telemetry exports are disabled during CI tests.
- AWS OIDC authentication is planned for deployment.

## Planned Improvements

- Terraform infrastructure provisioning
- AWS Lambda deployment
- HTTP API integration
- GitHub Actions CD pipeline
- Cloud-hosted log collection
