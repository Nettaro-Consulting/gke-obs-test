import logging
import os
import time

from loki.handlers import LokiHandler
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

# --- Configuration ---
LOKI_URL = os.getenv("LOKI_URL", "https://loki.nettaro.com/loki/api/v1/push")
TEMPO_OTLP_HTTP_ENDPOINT = os.getenv("TEMPO_OTLP_HTTP_ENDPOINT", "https://tempo.nettaro.com/v1/traces")
SERVICE_NAME = "my-external-app"

# --- Loki Logger Setup ---
def setup_loki_logging():
    handler = LokiHandler(
        url=LOKI_URL,
        tags={"application": SERVICE_NAME, "environment": "development"},
        version="1",
    )
    logger = logging.getLogger(SERVICE_NAME)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    return logger

# --- OpenTelemetry Tracing Setup ---
def setup_tempo_tracing():
    resource = Resource.create({
        "service.name": SERVICE_NAME,
        "service.instance.id": "instance-1",
    })
    provider = TracerProvider(resource=resource)
    processor = BatchSpanProcessor(
        OTLPSpanExporter(endpoint=TEMPO_OTLP_HTTP_ENDPOINT)
    )
    provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)
    return trace.get_tracer(SERVICE_NAME)

# --- Main Application Logic ---
if __name__ == "__main__":
    # Setup logging
    logger = setup_loki_logging()
    logger.info("Loki logger initialized.")

    # Setup tracing
    tracer = setup_tempo_tracing()
    logger.info("Tempo tracer initialized.")

    print(f"Sending logs to: {LOKI_URL}")
    print(f"Sending traces to: {TEMPO_OTLP_HTTP_ENDPOINT}")
    print("Generating sample telemetry data...")

    for i in range(3):
        with tracer.start_as_current_span(f"operation-{i}") as span:
            span.set_attribute("iteration", i)
            logger.info(f"Starting operation {i}...")
            time.sleep(0.1) # Simulate some work

            with tracer.start_as_current_span(f"sub-operation-{i}"):
                logger.debug(f"Executing sub-operation {i}...")
                time.sleep(0.05) # Simulate more work
                span.set_attribute("sub_operation_status", "completed")

            logger.info(f"Finished operation {i}.")
            span.set_attribute("operation_status", "success")

    logger.info("Sample telemetry data sent. Check Loki and Tempo for data.")
    print("Sample telemetry data sent. Check Loki and Tempo for data.")

    # Give exporters a moment to flush data
    time.sleep(2)
