#!/bin/bash

set -e

echo "🚀 PoV Sim Setup"
echo "----------------"

# ── Homebrew ────────────────────────────────────────────────────────────────
if ! command -v brew &>/dev/null; then
  echo "❌ Homebrew is not installed. Install it from https://brew.sh and re-run this script."
  exit 1
fi
echo "✅ Homebrew detected"

# ── Docker CLI ───────────────────────────────────────────────────────────────
if ! command -v docker &>/dev/null; then
  echo "📦 Installing Docker CLI..."
  brew install docker
else
  echo "✅ Docker CLI detected"
fi

# ── Docker Compose plugin ────────────────────────────────────────────────────
if ! docker compose version &>/dev/null 2>&1; then
  echo "📦 Installing docker-compose plugin..."
  brew install docker-compose
  mkdir -p ~/.docker/cli-plugins
  ln -sfn /opt/homebrew/opt/docker-compose/bin/docker-compose ~/.docker/cli-plugins/docker-compose
else
  echo "✅ docker-compose plugin detected"
fi

# ── Docker Buildx plugin ─────────────────────────────────────────────────────
if ! docker buildx version &>/dev/null 2>&1; then
  echo "📦 Installing docker-buildx plugin..."
  brew install docker-buildx
  mkdir -p ~/.docker/cli-plugins
  ln -sfn /opt/homebrew/opt/docker-buildx/bin/docker-buildx ~/.docker/cli-plugins/docker-buildx
  docker buildx create --use
else
  echo "✅ docker-buildx plugin detected"
fi

# ── Docker daemon (Colima or Docker Desktop) ─────────────────────────────────
if ! docker info &>/dev/null 2>&1; then
  echo "🐳 No Docker daemon detected. Checking for Colima..."
  if ! command -v colima &>/dev/null; then
    echo "📦 Installing Colima..."
    brew install colima
  fi
  echo "▶️  Starting Colima..."
  colima start
else
  echo "✅ Docker daemon is running"
fi

# ── .env file ────────────────────────────────────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"

if [ ! -f "$REPO_ROOT/.env" ]; then
  echo "📄 Creating .env from .env_EXAMPLE..."
  cp "$REPO_ROOT/.env_EXAMPLE" "$REPO_ROOT/.env"
else
  echo "✅ .env file already exists"
fi

echo ""
echo "✅ Setup complete! Run 'make up' to start the services."
