#! /usr/bin/env bash

docker buildx build . -t lake_temp \
	&& docker run --name lake_temp -it lake_temp \
	&& docker rm lake_temp \
	&& docker rmi lake_temp

