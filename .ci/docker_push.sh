#!/bin/bash
docker build -t reflexer/auction-keeper .
echo "${DOCKER_PASSWORD}" | docker login -u "${DOCKER_USERNAME}" --password-stdin
docker tag reflexer/auction-keeper reflexer/auction-keeper:${COMMIT}
docker push reflexer/auction-keeper
docker push reflexer/auction-keeper:${COMMIT}
