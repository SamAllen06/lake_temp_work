#! /usr/bin/env bash

docker buildx build . -t lake_temp

if [ $? -eq 0 ]; then
	docker run --name lake_temp -it lake_temp 
	if [ $? -eq 0 ]; then
		docker rm lake_temp
	fi
	docker rmi lake_temp
fi

