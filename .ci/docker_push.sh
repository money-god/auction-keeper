#!/bin/bash
docker build -t reflexer/auction-keeper:test .
echo "${DOCKER_PASSWORD}" | docker login -u "${DOCKER_USERNAME}" --password-stdin
docker tag reflexer/auction-keeper:test reflexer/auction-keeper:${COMMIT}
docker push reflexer/auction-keeper:test
docker push reflexer/auction-keeper:${COMMIT}
