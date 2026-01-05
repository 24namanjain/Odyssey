---
notion_page_id: 2deff901-fc97-817e-9d9d-da6668903853
title: docker-basic-commands
---

# Docker Basic Commands

## Pulling and Running PostgreSQL

```bash
docker run postgres:17.2
# Unable to find image 'postgres:17.2' locally
# Pulling the image from Docker Hub
# Error: Database is uninitialized and superuser password is not specified

docker run -e POSTGRES_PASSWORD=admin postgres:17.2
# Successfully initializes and starts PostgreSQL

```

## Running PostgreSQL in Detached Mode

```bash
docker run -d -e POSTGRES_PASSWORD=admin postgres:17.2
# Runs PostgreSQL in detached mode

```

## Pulling Redis Image

```bash
docker pull redis
# Pulls the latest Redis image from Docker Hub

```

## Listing All Containers

```bash
docker ps -a
# Lists all containers, including stopped ones

```

## Listing Docker Images

```bash
docker images
# Lists all Docker images

```

## Running Redis

```bash
docker run redis:7.4.2
# Pulls and runs Redis version 7.4.2

docker run -d redis:7.4.2
# Runs Redis in detached mode

docker run -p6000:6379 -d redis
# Runs Redis and maps port 6000 on the host to port 6379 in the container

docker run -p6001:6379 -d redis:7.4.2
# Runs Redis version 7.4.2 and maps port 6001 on the host to port 6379 in the container

```

## Stopping and Starting Containers

```bash
docker stop <container_id>
# Stops a running container

docker start <container_id>
# Starts a stopped container

```

## Removing Containers

```bash
docker rm <container_id>
# Removes a stopped container
```