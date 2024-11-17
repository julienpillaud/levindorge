if [ "$1" = "stop" ]; then
    echo "🛑 Stopping development environment..."
    docker compose -f compose-dev.yaml down
    exit 0
fi

echo "🚀 Starting development environment..."
docker compose -f compose-dev.yaml watch
