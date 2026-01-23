default:
    just --list

build tag:
    docker buildx build \
    --platform linux/amd64,linux/arm64 \
    -t ghcr.io/julienpillaud/levindorge:{{ tag }} \
    .

push tag:
    docker push ghcr.io/julienpillaud/levindorge:{{ tag }}

prod:
    IMAGE_TAG=dev \
    HOST=app.localhost \
    docker compose -f compose-prod.yaml up -d

traefik:
    DOMAIN=app.localhost \
    USERNAME=admin \
    HASHED_PASSWORD=$(openssl passwd -apr1 admin) \
    docker compose -f compose-traefik.yaml up -d

mongodb container_name="mongodb" \
        port="27017" \
        user="user" \
        password="password":
    docker run -d \
    --name {{container_name}} \
    -p {{port}}:27017 \
    -e MONGO_INITDB_ROOT_USERNAME={{user}} \
    -e MONGO_INITDB_ROOT_PASSWORD={{password}} \
    --restart unless-stopped \
    mongo:latest


run-app:
    uv run uvicorn app.core.app:app --reload --proxy-headers --log-config app/core/logging/config.json

run-worker:
    uv run faststream run app.core.event_handler:app --workers 3
