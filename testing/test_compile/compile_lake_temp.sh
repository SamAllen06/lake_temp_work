#!/usr/bin/env bash

set -e

docker buildx build -t lake_temp_compile ./
docker run --name lake_temp_compile --volume ./result:/mnt/result lake_temp_compile
docker rm lake_temp_compile
docker rmi lake_temp_compile
