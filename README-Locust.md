# Locust Load Testing Guide

## Overview
Locust is an open-source load testing tool written in Python. It allows you to write test scenarios in Python code and provides a web interface to monitor and control load tests in real-time.

## Prerequisites

### 1. Install Python and pip
```bash
# For CentOS/RHEL
sudo yum install python3 python3-pip

# For Ubuntu/Debian
sudo apt-get install python3 python3-pip
```

### 2. Install Locust
```bash
# Install globally
pip3 install locust

# Or create virtual environment (recommended)
python3 -m venv locust_env
source locust_env/bin/activate
pip install locust
```

## Quick Start

### 1. Basic Command
```bash
locust -f locustfile.py --host=http://192.168.11.12:8888 --web-port=9999
```

**Parameter Explanation:**
- `-f locustfile.py`: Specifies the test file to use
- `--host=http://192.168.11.12:8888`: Target API endpoint (KrakenD gateway)
- `--web-port=9999`: Port for Locust web interface

### 2. Access Web Interface
After starting Locust, open your browser and go to:
```
http://localhost:9999
```

## Test Scenarios

### Current Test File (`locustfile.py`)
The current test file includes two scenarios:

1. **GET /v1/movie** - Basic movie list retrieval
2. **GET /v1/movie?title=star&limit=10** - Search with parameters (runs 2x more frequently)

```python
from locust import HttpUser, task, between

class MovieAPIUser(HttpUser):
    wait_time = between(1, 3)  # Wait 1-3 seconds between requests
    
    @task
    def get_movies(self):
        self.client.get("/v1/movie", headers={
            "Accept": "application/json",
            "Content-Type": "application/json"
        })
    
    @task(2)  # This task runs 2x more frequently
    def get_movies_with_params(self):
        self.client.get("/v1/movie?title=star&limit=10", headers={
            "Accept": "application/json",
            "Content-Type": "application/json"
        })
```

## Running Load Tests

### Method 1: Command Line Interface
```bash
# Basic run
locust -f locustfile.py --host=http://192.168.11.12:8888 --web-port=9999

# Run with specific parameters
locust -f locustfile.py \
  --host=http://192.168.11.12:8888 \
  --web-port=9999 \
  --users=100 \
  --spawn-rate=10 \
  --run-time=60s
```

### Method 2: Web Interface
1. Start Locust: `locust -f locustfile.py --host=http://192.168.11.12:8888 --web-port=9999`
2. Open browser: `http://localhost:9999`
3. Configure test parameters:
   - **Number of users**: 100
   - **Spawn rate**: 10 users/second
   - **Host**: http://192.168.11.12:8888
4. Click "Start swarming"

### Method 3: Docker (if available)
```bash
# Build and run Locust container
docker build -t locust-loadtest ./locust
docker run -p 8089:8089 locust-loadtest
```

## Test Parameters

### Common Parameters
- `--users`: Number of concurrent users (default: 1)
- `--spawn-rate`: Users spawned per second (default: 1)
- `--run-time`: Test duration (e.g., "60s", "5m", "1h")
- `--web-port`: Web interface port (default: 8089)
- `--host`: Target host URL

### Example Scenarios

#### Light Load Test
```bash
locust -f locustfile.py \
  --host=http://192.168.11.12:8888 \
  --users=10 \
  --spawn-rate=2 \
  --run-time=60s \
  --web-port=9999
```

#### Medium Load Test
```bash
locust -f locustfile.py \
  --host=http://192.168.11.12:8888 \
  --users=50 \
  --spawn-rate=5 \
  --run-time=300s \
  --web-port=9999
```

#### Heavy Load Test
```bash
locust -f locustfile.py \
  --host=http://192.168.11.12:8888 \
  --users=200 \
  --spawn-rate=20 \
  --run-time=600s \
  --web-port=9999
```

## Understanding Results

### Key Metrics
- **RPS (Requests Per Second)**: How many requests your API can handle
- **Response Time**: Average, median, 95th percentile response times
- **Failure Rate**: Percentage of failed requests
- **User Count**: Number of concurrent users

### Interpreting Results
- **Good Performance**: < 200ms average response time, < 1% failure rate
- **Acceptable Performance**: < 500ms average response time, < 5% failure rate
- **Poor Performance**: > 1000ms average response time, > 10% failure rate

## Troubleshooting

### Common Issues

#### 1. Port Already in Use
```bash
# Error: OSError: [Errno 98] Address already in use
# Solution: Use different port
locust -f locustfile.py --host=http://192.168.11.12:8888 --web-port=9999
```

#### 2. Connection Timeouts
```bash
# Check if API is accessible
curl -v http://192.168.11.12:8888/v1/movie

# Check KrakenD logs
docker logs krakend
```

#### 3. High Failure Rate
- Check API logs: `docker logs flask_api`
- Check MongoDB logs: `docker logs my_mongodb`
- Verify KrakenD configuration

### Debug Mode
```bash
# Run with verbose logging
locust -f locustfile.py --host=http://192.168.11.12:8888 --web-port=9999 --loglevel=DEBUG
```

## Advanced Usage

### Custom Test Scenarios
Create your own test file:

```python
from locust import HttpUser, task, between

class CustomAPIUser(HttpUser):
    wait_time = between(1, 5)
    
    @task
    def test_get_movie_by_id(self):
        self.client.get("/v1/movie/507f1f77bcf86cd799439011")
    
    @task
    def test_search_movies(self):
        self.client.get("/v1/movie?genre=action&year=2020&limit=5")
    
    @task
    def test_post_movie(self):
        movie_data = {
            "title": "Test Movie",
            "year": 2024,
            "genre": "Test"
        }
        self.client.post("/v1/movie", json=movie_data)
```

### Headless Mode (No Web UI)
```bash
locust -f locustfile.py \
  --host=http://192.168.11.12:8888 \
  --users=100 \
  --spawn-rate=10 \
  --run-time=60s \
  --headless \
  --csv=results
```

### Distributed Testing
```bash
# Master node
locust -f locustfile.py --master --master-bind-host=0.0.0.0

# Worker nodes
locust -f locustfile.py --worker --master-host=<master-ip>
```

## Integration with Monitoring

### Prometheus Metrics
Locust can export metrics to Prometheus:
```bash
locust -f locustfile.py \
  --host=http://192.168.11.12:8888 \
  --web-port=9999 \
  --enable-statsd \
  --statsd-host=prometheus
```

### Grafana Dashboard
Create a Grafana dashboard to visualize:
- Request rate over time
- Response time percentiles
- Error rates
- User count trends

## Best Practices

1. **Start Small**: Begin with low user counts and gradually increase
2. **Monitor Resources**: Watch CPU, memory, and network usage
3. **Test Realistic Scenarios**: Simulate actual user behavior
4. **Use Different Test Types**:
   - Smoke test: 1-5 users
   - Load test: 10-100 users
   - Stress test: 100+ users
5. **Document Results**: Keep records of test configurations and results

## Example Test Session

```bash
# 1. Start Locust
locust -f locustfile.py --host=http://192.168.11.12:8888 --web-port=9999

# 2. Open browser: http://localhost:9999

# 3. Configure test:
#    - Number of users: 50
#    - Spawn rate: 5 users/second
#    - Host: http://192.168.11.12:8888

# 4. Click "Start swarming"

# 5. Monitor results in real-time

# 6. Stop test when complete

# 7. Review final statistics
```

## Useful Commands

```bash
# Check if port is available
netstat -tulpn | grep 9999

# Kill process using port
sudo fuser -k 9999/tcp

# Check Locust version
locust --version

# Get help
locust --help
```

## Next Steps

1. **Create More Test Scenarios**: Add POST, PUT, DELETE operations
2. **Parameterize Tests**: Use different search terms and parameters
3. **Add Assertions**: Verify response content and status codes
4. **Integrate with CI/CD**: Automate load testing in your pipeline
5. **Set Up Monitoring**: Configure alerts for performance thresholds 