# Microservices with Observability in Kubernetes

This project implements a simple two-service application deployed on Kubernetes, with integrated observability tools such as Prometheus for metrics and Jaeger for tracing.

The application consists of two microservices:

- **Hash Service**: Computes the SHA256 hash of an input string.
- **Length Service**: Computes the length of an input string.

The goal is to implement observability using **Prometheus** for monitoring and **Jaeger** for tracing in a Kubernetes environment.

---

## **Setup Instructions**

1. Clone the Repository
Clone the repository to your local machine and navigate to the project directory:
```bash
git clone <repository-url>
cd <repository-folder>
```

2. Build and Push Docker Images

Build the Docker images for both services and push them to your container registry:

```bash
docker build -t <your-registry>/hash-service:latest .
docker build -t <your-registry>/length-service:latest .
docker push <your-registry>/hash-service:latest
docker push <your-registry>/length-service:latest
```

3. Deploy to Kubernetes
Apply the Kubernetes manifests to deploy the services and other configurations:

```bash
kubectl apply -f kubernetes/
```

4. Install Prometheus and Jaeger using Helm

Use Helm to deploy Prometheus and Jaeger for monitoring and tracing:

```bash
helm install prometheus prometheus-community/prometheus
helm install jaeger jaegertracing/jaeger
Example API Requests
Once your services are up, you can interact with them using curl or Postman.
```

Hash Service:

```bash
curl -X POST http://localhost:8080/hash -d "Apple"
```

This will return a JSON object with the SHA256 hash of the input string:

```bash
{"hash": "f223faa96f22916294922b171a2696d868fd1f9129302eb41a45b2a2ea2ebbfd"}
```

Length Service:
```bash
curl -X POST http://localhost:8081/length -d "Apple"
```

This will return the length of the input string:

```bash
{"length": 5}
```

Observbility

helm install prometheus ./prometheus

helm install jaeger ./jaeger


Viewing Traces
To observe the flow of requests across services and inspect distributed traces:

Open the Jaeger UI at:

```bash
http://<jaeger-url>/search
```

Here, you can search for traces related to your service calls and view detailed tracing information.

Viewing Metrics
For monitoring the application’s performance, use Prometheus to view real-time metrics.

Access the Prometheus dashboard at:

```bash
http://<prometheus-url>/graph
```

You can query various metrics such as request duration, success/failure rates, and more.


Optional Improvements
Enhance your project further with the following optional improvements:

Security: Implement HTTPS with SSL/TLS and use token-based authentication for secure API access.
CI/CD Pipeline: Automate the deployment process using tools like GitLab CI, Jenkins, or GitHub Actions.
Custom Dashboards: Use Grafana to create custom dashboards for visualizing the metrics collected by Prometheus.
Scalability & Resilience: Scale the services horizontally and implement fault tolerance mechanisms in Kubernetes for high availability.


prometheus:

helm search hub Prometheus
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm install prometheus prometheus-community/prometheus

otel and jaeger

helm repo add jaegertracing https://jaegertracing.github.io/helm-charts
helm repo update
helm search repo jaegertracing/jaeger
 helm upgrade --install jaeger jaegertracing/jaeger
 helm upgrade --install jaeger jaegertracing/jaeger    --set query.resources.requests.memory=512Mi   --set query.resources.limits.memory=1Gi    --set collector.resources.requests.memory=512Mi   --set collector.resources.limits.memory=1Gi    --set query.healthCheck.readinessProbe.enabled=false
helm upgrade --install jaeger jaegertracing/jaeger  --values jaeger.yaml **


helm repo add open-telemetry https://open-telemetry.github.io/opentelemetry-helm-charts
helm repo update
helm show values open-telemetry/opentelemetry-collector > otel.yaml
helm install otel-collector open-telemetry/opentelemetry-collector --values otel-collector-values.yaml --set image.repository="otel/opentelemetry-collector-k8s"

https://medium.com/@blackhorseya/deploying-opentelemetry-and-jaeger-with-helm-on-kubernetes-d86cc8ba0332
helm install jaeger jaegertracing/jaeger




helm install jaeger ./
helm install prometheus ./

kubectl port-forward svc/prometheus 9090:9090

http://localhost:9090


helm install jaeger ./
kubectl port-forward svc/jaeger 16686:16686
http://localhost:16686


helm upgrade prometheus ./prometheus-chart


curl -X POST http://localhost:8080/hash  -H "Content-Type: application/json" -d "{\"text\": \"Apple\"}"
