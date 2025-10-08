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
