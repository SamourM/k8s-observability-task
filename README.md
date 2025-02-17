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
git clone git@github.com:SamourM/k8s-observability-task.git
cd k8s-observability-task.git
```

2. Build and Push Docker Images

Build the Docker images for both services and push them to your container registry:

```bash
docker build -t <your-registry>/hash-service:latest .
docker build -t <your-registry>/length-service:latest .
docker push <your-registry>/hash-service:latest
docker push <your-registry>/length-service:latest
```

3. Deploy Services to Kubernetes
Apply the Kubernetes manifests to deploy the services and other configurations:

```bash
kubectl apply -f <k8s-templates yaml files>
```

4. Install Prometheus and Jaeger using Helm

Use Helm to deploy Prometheus and Jaeger for monitoring and tracing:

```bash
helm install prometheus .\prometheus\
helm install jaeger .\jaeger\
helm install otel .\otel\
helm install grafana .\grafana\
```
## **Example Requests**

Hash Service:

```bash
curl -X POST http://localhost:8080/hash  -H "Content-Type: application/json" -d "{\"text\": \"Apple\"}"
```

This will return a JSON object with the SHA256 hash of the input string:

```bash
{"hash": "f223faa96f22916294922b171a2696d868fd1f9129302eb41a45b2a2ea2ebbfd"}
```

Length Service:
```bash
curl -X POST http://localhost:8081/length  -H "Content-Type: application/json" -d "{\"text\": \"Apple\"}"
```

This will return the length of the input string:

```bash
{"length": 5}
```

## **Observability - View Traces and Metrics**

To observe the flow of requests across services and inspect distributed traces:

Open the Jaeger UI at:

```bash
http://<jaeger-url>:16686
```

Here, you can search for traces related to your service calls and view detailed tracing information.

Viewing Metrics
For monitoring the application’s performance, use Prometheus to view real-time metrics.

Access the Prometheus dashboard at:

```bash
http://<prometheus-url>:9090
http://<grafana-url>:3000
```

You can query various metrics such as request duration, success/failure rates, and more.


## **Optional Improvements**

Enhance your project further with the following optional improvements:

Security: Implement HTTPS with SSL/TLS and use token-based authentication for secure API access.

CI/CD Pipeline: Automate the deployment process using tools like GitLab CI, Jenkins, or GitHub Actions, I added one gitlab ci example in this repo.

Custom Dashboards: Use Grafana to create custom dashboards for visualizing the metrics collected by Prometheus, I implemented grafana with prometheus as datasource.

Scalability & Resilience: Scale the services horizontally and implement fault tolerance mechanisms in Kubernetes for high availability, like using HPA, BDP ..etc.



## **Snippets**

Please refer to snippet folder.









