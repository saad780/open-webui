#!/usr/bin/env bash
set -euo pipefail

# ---------------------------------------------------------------------------
# Build and run the Open WebUI Docker container locally.
# ---------------------------------------------------------------------------

readonly IMAGE="open-webui"
readonly CONTAINER="open-webui"
readonly HOST_PORT="${OPEN_WEBUI_PORT:-3000}"
readonly CONTAINER_PORT=8080
readonly HOST_HOME="${OPEN_WEBUI_HOST_HOME:-/home/spark}"
readonly LOCAL_FILES="${OPEN_WEBUI_LOCAL_FILES:-/home/spark/openwebui-files}"

echo "Building ${IMAGE} image..."
docker build -t "$IMAGE" .

echo "Stopping any existing ${CONTAINER} container..."
docker stop "$CONTAINER" 2>/dev/null || true
docker rm "$CONTAINER" 2>/dev/null || true

mkdir -p "$LOCAL_FILES"

echo "Starting ${CONTAINER}..."
docker run -d \
  -p "${HOST_PORT}:${CONTAINER_PORT}" \
  --add-host=host.docker.internal:host-gateway \
  -v "${IMAGE}:/app/backend/data" \
  -v "${HOST_HOME}:/mnt/host-home:ro" \
  -v "${LOCAL_FILES}:/mnt/local-files:rw" \
  --name "$CONTAINER" \
  --restart always \
  "$IMAGE"

echo "Cleaning up dangling images..."
docker image prune -f

echo "Open WebUI is running at http://localhost:${HOST_PORT}"
