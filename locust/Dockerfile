FROM python:3.9-slim

WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir locust

# Copy locust files
COPY . .

# Expose port
EXPOSE 8089

# Run locust
CMD ["locust", "--host=http://192.168.11.12:8888", "--port=8089"] 