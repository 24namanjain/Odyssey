# Debugging a Docker Container

## Listing Running Containers
```bash
docker ps
# Lists all running containers
```

## Viewing Logs of a Container
```bash
docker logs 4e581427f272
# Displays logs for the container with ID 4e581427f272
```

## Stopping a Container
```bash
docker stop 4e581427f272
# Stops the container with ID 4e581427f272
```

## Running an Older Version of Redis
```bash
docker run -d -p6001:6379 --name redis-older redis:4.0
# Runs Redis version 4.0 in detached mode and maps port 6001 on the host to port 6379 in the container
```

## Viewing Logs of the New Container
```bash
docker logs redis-older
# Displays logs for the container named redis-older
```

## Executing Commands Inside a Running Container
```bash
docker exec -it dee2f89027e3 /bin/bash
# Opens a bash shell inside the container with ID dee2f89027e3

# Inside the container
ls
# Lists files and directories in the current directory

pwd
# Prints the current working directory

cd ~
# Changes to the home directory

cd /
# Changes to the root directory

ls
# Lists files and directories in the root directory

env
# Displays environment variables
```