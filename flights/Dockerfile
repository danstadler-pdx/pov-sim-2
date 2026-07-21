FROM python:3.8-slim-buster

WORKDIR /python-docker

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

# Install OTel instrumentation packages for libraries detected in the env.
# Picks up Flask, requests, urllib3, logging, etc.
RUN opentelemetry-bootstrap -a install

COPY . .

EXPOSE 5001

# Wrap Flask with opentelemetry-instrument so spans/metrics/logs are emitted
# without code changes. Service identity comes from OTEL_* env vars set in
# docker-compose.yml.
CMD ["opentelemetry-instrument", "python3", "-m", "flask", "run", "--host=0.0.0.0", "--port=5001"]
