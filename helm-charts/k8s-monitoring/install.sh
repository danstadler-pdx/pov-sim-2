#!/usr/bin/env bash
# Stage 3.1 — install/upgrade the Grafana Kubernetes Monitoring Helm chart.
#
# Renders values.yaml through envsubst so the auth token (loaded from ../.env)
# never lives in the committed YAML. Run from anywhere; the script cd's into
# its own dir.
set -euo pipefail

cd "$(dirname "$0")"

# Load .env from the repo root if present.
if [ -f "../../.env" ]; then
  set -a
  # shellcheck disable=SC1091
  . ../../.env
  set +a
fi

: "${CLOUD_K8S_MONITORING_TOKEN:?CLOUD_K8S_MONITORING_TOKEN must be set (put it in .env)}"

helm repo add grafana https://grafana.github.io/helm-charts >/dev/null
helm repo update >/dev/null

envsubst < values.yaml | helm upgrade --install \
  --rollback-on-failure --timeout 300s \
  --namespace default --create-namespace \
  --version "^4" \
  --values - \
  grafana-k8s-monitoring grafana/k8s-monitoring
