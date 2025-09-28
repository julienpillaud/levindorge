default:
    just --list

build tag:
    docker buildx build \
    --platform linux/amd64,linux/arm64 \
    -t ghcr.io/julienpillaud/levindorge:{{ tag }} \
    .

push tag:
    docker push ghcr.io/julienpillaud/levindorge:{{ tag }}
