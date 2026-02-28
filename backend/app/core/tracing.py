"""OpenTelemetry tracing setup (optional).

Initialises the OpenTelemetry SDK with console or OTLP exporter when
the ``OTEL_EXPORTER_OTLP_ENDPOINT`` environment variable is set.

Usage in ``main.py``::

    from app.core.tracing import setup_tracing
    setup_tracing(app)
"""

import os
from typing import TYPE_CHECKING

from app.core.logging import get_logger

if TYPE_CHECKING:
    from fastapi import FastAPI

logger = get_logger("tracing")


def setup_tracing(app: "FastAPI") -> None:
    """Configure OpenTelemetry tracing if dependencies are available.

    Silently skips if opentelemetry packages are not installed.
    """
    try:
        from opentelemetry import trace
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.resources import Resource
        from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

        resource = Resource.create({"service.name": "quiz-forge-api"})
        provider = TracerProvider(resource=resource)

        otlp_endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")
        if otlp_endpoint:
            from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
            from opentelemetry.sdk.trace.export import BatchSpanProcessor

            exporter = OTLPSpanExporter(endpoint=otlp_endpoint)
            provider.add_span_processor(BatchSpanProcessor(exporter))
            logger.info("OTLP tracing enabled → %s", otlp_endpoint)
        else:
            from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor

            provider.add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))
            logger.info("Console tracing enabled (set OTEL_EXPORTER_OTLP_ENDPOINT for OTLP)")

        trace.set_tracer_provider(provider)
        FastAPIInstrumentor.instrument_app(app)
        logger.info("OpenTelemetry instrumentation applied")

    except ImportError:
        logger.debug("OpenTelemetry packages not installed, skipping tracing setup")
