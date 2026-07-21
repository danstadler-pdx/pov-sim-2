FROM gradle:8.3.0-jdk17 AS build

WORKDIR /app
COPY . .
RUN gradle clean bootJar

# Download both Java agents in the build stage (keeps the final image slim).
# Stage 2.1: OpenTelemetry Java agent (traces, metrics, logs to Alloy → Cloud).
ADD https://github.com/open-telemetry/opentelemetry-java-instrumentation/releases/download/v2.10.0/opentelemetry-javaagent.jar /agent/opentelemetry-javaagent.jar
# Stage 2.2: Pyroscope Java agent (continuous profiling direct to Cloud Pyroscope).
ADD https://github.com/grafana/pyroscope-java/releases/download/v2.1.2/pyroscope.jar /agent/pyroscope.jar

FROM eclipse-temurin:17-jdk-alpine

WORKDIR /app
COPY --from=build /app/build/libs/*.jar app.jar
COPY --from=build /agent/opentelemetry-javaagent.jar /agent/opentelemetry-javaagent.jar
COPY --from=build /agent/pyroscope.jar /agent/pyroscope.jar

EXPOSE 8080

# Two javaagents — OTel first, Pyroscope second. JVM applies them in order.
# All identity + endpoint config comes from env vars set in docker-compose.yml
# (OTEL_* for the OTel agent, PYROSCOPE_* for the Pyroscope agent).
ENTRYPOINT ["java", "-javaagent:/agent/opentelemetry-javaagent.jar", "-javaagent:/agent/pyroscope.jar", "-jar", "app.jar"]
