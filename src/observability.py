
import os
import base64

from dotenv import load_dotenv

from opentelemetry import trace, metrics
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import (
    PeriodicExportingMetricReader,
)

from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
    OTLPSpanExporter,
)
from opentelemetry.exporter.otlp.proto.http.metric_exporter import (
    OTLPMetricExporter,
)

load_dotenv()

TELEMETRY_ENABLED = (
    os.getenv("TELEMETRY_ENABLED", "true").lower() == "true"
)

resource = Resource.create({
    "service.name": "devops-lambda-assignment",
    "deployment.environment": os.getenv(
        "DEPLOYMENT_ENVIRONMENT", "local"
    ),
})

trace_provider = TracerProvider(resource=resource)
meter_provider = None

if TELEMETRY_ENABLED:
    endpoint = os.getenv("GRAFANA_OTLP_ENDPOINT", "").rstrip("/")
    instance_id = os.getenv("GRAFANA_INSTANCE_ID", "")
    api_token = os.getenv("GRAFANA_API_TOKEN", "")

    if not all([endpoint, instance_id, api_token]):
        raise RuntimeError(
            "Missing Grafana Cloud environment variables"
        )

    credentials = f"{instance_id}:{api_token}"
    encoded_credentials = base64.b64encode(
        credentials.encode("utf-8")
    ).decode("utf-8")

    headers = {
        "Authorization": f"Basic {encoded_credentials}"
    }

    trace_exporter = OTLPSpanExporter(
        endpoint=f"{endpoint}/v1/traces",
        headers=headers,
        timeout=10,
    )

    trace_provider.add_span_processor(
        BatchSpanProcessor(trace_exporter)
    )

    metric_exporter = OTLPMetricExporter(
        endpoint=f"{endpoint}/v1/metrics",
        headers=headers,
        timeout=10,
    )

    metric_reader = PeriodicExportingMetricReader(
        metric_exporter,
        export_interval_millis=10000,
    )

    meter_provider = MeterProvider(
        resource=resource,
        metric_readers=[metric_reader],
    )
else:
    meter_provider = MeterProvider(resource=resource)

trace.set_tracer_provider(trace_provider)
metrics.set_meter_provider(meter_provider)

tracer = trace.get_tracer("order-api")
meter = metrics.get_meter("order-api")

request_counter = meter.create_counter(
    "order_api_requests",
    description="Total API requests",
    unit="1",
)

error_counter = meter.create_counter(
    "order_api_errors",
    description="Total server errors",
    unit="1",
)

duration_histogram = meter.create_histogram(
    "order_api_duration",
    description="API request duration",
    unit="ms",
)


def record_request(method, path, status_code, duration_ms):
    attributes = {
        "http.request.method": method,
        "url.path": path,
        "http.response.status_code": status_code,
    }

    request_counter.add(1, attributes)

    if status_code >= 500:
        error_counter.add(1, attributes)

    duration_histogram.record(duration_ms, attributes)


def flush_telemetry():
    if not TELEMETRY_ENABLED:
        return True

    traces_ok = trace_provider.force_flush(timeout_millis=15000)
    metrics_ok = meter_provider.force_flush(timeout_millis=15000)

    return traces_ok and metrics_ok

