#!/bin/bash

# Stop and remove all running containers and networks created by docker-compose
docker-compose down

# Build the Docker images defined in the docker-compose.yml file
docker-compose build

# Start the services defined in the docker-compose.yml file
docker-compose up
