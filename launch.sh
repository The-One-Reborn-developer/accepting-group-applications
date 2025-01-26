#!/bin/bash

# Bring down the existing environment
sudo docker-compose -f dockerfiles/docker-compose.yml down -v

# Build the image
sudo docker-compose -f dockerfiles/docker-compose.yml build

# Bring up the environment
sudo docker-compose -f dockerfiles/docker-compose.yml up
