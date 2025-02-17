from flask import Flask, request, jsonify
import time

# Prometheus imports
from prometheus_client import Counter, Histogram, generate_latest, REGISTRY
from prometheus_client.exposition import make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware

# OpenTelemetry imports
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# Initialize Flask app
app = Flask(__name__)

# Instrument Flask with OpenTelemetry
FlaskInstrumentor().instrument_app(app)

# Initialize OpenTelemetry tracing
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

# Configure Jaeger Exporter
jaeger_exporter = JaegerExporter(
    agent_host_name="jaeger",  # Change this to the correct hostname if needed
    agent_port=6831
)
trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(jaeger_exporter))

# Prometheus Metrics
REQUEST_COUNT = Counter('length_requests_total', 'Total length calculation requests', ['method', 'endpoint'])
REQUEST_LATENCY = Histogram('length_request_latency_seconds', 'Request latency in seconds', ['method', 'endpoint'])

@app.route('/length', methods=['POST'])
def calculate_length():
    REQUEST_COUNT.labels(method='POST', endpoint='/length').inc()
    start_time = time.time()

    with tracer.start_as_current_span("calculate_length"):
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

            # Calculate length
            text_length = len(input_string)

            return jsonify({"length": text_length})

        except Exception as e:
            return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500
        finally:
            REQUEST_LATENCY.labels(method='POST', endpoint='/length').observe(time.time() - start_time)

# Health Check Endpoint
@app.route('/health', methods=['GET'])
def health_check():
    return "OK", 200

# Expose Prometheus metrics at `/metrics`
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    "/metrics": make_wsgi_app(REGISTRY)
})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)  # Running on port 8081 to avoid conflicts
