from flask import Flask, request, jsonify
import hashlib
import time

# Prometheus imports
from prometheus_client import Counter, Histogram, generate_latest, REGISTRY
from prometheus_client.exposition import make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware

# OpenTelemetry imports
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor

# Initialize Flask app
app = Flask(__name__)

# Instrument Flask with OpenTelemetry
FlaskInstrumentor().instrument_app(app)

# Initialize OpenTelemetry tracing
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

# Configure OTLP Exporter
otlp_exporter = OTLPSpanExporter(
    endpoint="otel-collector:4317",  # OTLP endpoint, replace 'otel-collector' with your Jaeger Collector hostname
    insecure=True  # If your OTLP endpoint does not require encryption
)
trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(otlp_exporter))

# Prometheus Metrics
REQUEST_COUNT = Counter('hash_requests_total', 'Total hash requests', ['method', 'endpoint'])
REQUEST_LATENCY = Histogram('hash_request_latency_seconds', 'Request latency in seconds', ['method', 'endpoint'])

@app.route('/hash', methods=['POST'])
def hash_string():
    REQUEST_COUNT.labels(method='POST', endpoint='/hash').inc()
    start_time = time.time()

    with tracer.start_as_current_span("hash_string"):
        try:
            # Get the input data
            data = request.get_json()

            # Validate input
            if not data or 'text' not in data:
                return jsonify({"error": "Bad Request: 'text' field is required"}), 400

            input_string = data['text']

            # Check if input is a string
            if not isinstance(input_string, str):
                return jsonify({"error": "Bad Request: Input should be a string"}), 400

            # Generate the SHA256 hash
            hash_object = hashlib.sha256(input_string.encode())
            hash_hex = hash_object.hexdigest()

            return jsonify({"hash": hash_hex})

        except Exception as e:
            return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500
        finally:
            REQUEST_LATENCY.labels(method='POST', endpoint='/hash').observe(time.time() - start_time)

# Health Check Endpoint
@app.route('/health', methods=['GET'])
def health_check():
    return "OK", 200

# Expose Prometheus metrics at `/metrics`
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    "/metrics": make_wsgi_app(REGISTRY)
})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
