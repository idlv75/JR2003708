# 🐳 Docker Guide for Knight Journey

Complete guide for running Knight Journey in Docker containers.

---

## 📋 Prerequisites

- Docker 20.10+
- Docker Compose 2.0+ (optional)
- Make (optional, for convenience commands)

---

## 🚀 Quick Start

### Build the Image

```bash
# Using Make
make docker-build

# Using Docker directly
docker build -t knight-journey:latest .

# With custom Python version
docker build --build-arg PY_VER=3.12 -t knight-journey:latest .
```

### Run the Application

```bash
# Using Make
make docker-run INPUT_FILE=input.yaml

# Using Docker directly
docker run --rm -v $(pwd)/input.yaml:/app/input.yaml knight-journey:latest

# With custom input file
docker run --rm -v $(pwd)/my_input.yaml:/app/input.yaml \
    knight-journey:latest --input /app/input.yaml
```

---

## 🧪 Running Tests in Docker

```bash
# Using Make
make docker-test

# Using Docker directly
docker run --rm -v $(pwd):/app knight-journey:latest \
    pytest -v --cov=knight_journey
```

---

## 🔧 Development Mode

### Interactive Shell

```bash
# Using Make
make docker-shell

# Using Docker directly
docker run --rm -it -v $(pwd):/app knight-journey:latest bash
```

### Docker Compose Development

```bash
# Start development container
docker-compose --profile dev up -d dev

# Access shell
docker-compose exec dev bash

# Run application
docker-compose exec dev python -m knight_journey --input input.yaml

# Stop container
docker-compose down
```

---

## 📦 Multi-Stage Build

This project uses multi-stage Docker builds for:

1. **Smaller image size** - Runtime image excludes build dependencies
2. **Security** - Runs as non-root user
3. **Optimization** - Separate builder and runtime stages

### Build Stages

```
builder (stage 1) → runtime (stage 2)
    ↓                      ↓
Dependencies      Minimal production image
```

---

## 🎯 Docker Compose Profiles

### Available Profiles

| Profile | Purpose | Command |
|---------|---------|---------|
| default | Run application | `docker-compose up` |
| test | Run test suite | `docker-compose --profile test up test` |
| dev | Development shell | `docker-compose --profile dev up dev` |

### Examples

```bash
# Run app
docker-compose up app

# Run tests
docker-compose --profile test up test

# Development mode
docker-compose --profile dev up -d dev
docker-compose exec dev bash
```

---

## 🔐 Security Features

- ✅ Non-root user (`appuser`)
- ✅ Minimal base image (python:slim)
- ✅ No sensitive data in image
- ✅ Read-only file mounts
- ✅ Resource limits configured

---

## 📊 Image Information

```bash
# View image details
docker images knight-journey

# Inspect image
docker inspect knight-journey:latest

# View layers
docker history knight-journey:latest
```

---

## 🧹 Cleanup

```bash
# Remove image
make docker-clean

# Or manually
docker rmi knight-journey:latest

# Remove all unused Docker resources
docker system prune -a
```

---

## 🐛 Troubleshooting

### Permission Issues

```bash
# If you encounter permission errors
docker run --rm --user $(id -u):$(id -g) \
    -v $(pwd)/input.yaml:/app/input.yaml \
    knight-journey:latest
```

### Build Cache Issues

```bash
# Clear build cache
docker build --no-cache -t knight-journey:latest .
```

### Volume Mount Issues

```bash
# Verify volume mounts
docker run --rm -v $(pwd):/app knight-journey:latest ls -la /app
```


## 📝 Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PYTHON_VERSION` | 3.13 | Python version for build |
| `TAG` | latest | Docker image tag |
| `INPUT_FILE` | input.yaml | Default input file |

---

## 🔗 Integration with CI/CD

### GitHub Actions Example

```yaml
- name: Build Docker image
  run: docker build -t knight-journey:${{ github.sha }} .

- name: Run tests
  run: docker run knight-journey:${{ github.sha }} pytest

- name: Push to registry
  run: |
    docker tag knight-journey:${{ github.sha }} registry/knight-journey:latest
    docker push registry/knight-journey:latest
```

