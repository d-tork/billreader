#!/bin/bash

# Builds the docker image, passing the git hash as a build arg

cd ~/Documents/Python/bill-pdfs/
export GIT_HASH=$(git rev-parse HEAD)
docker build --build-arg GIT_HASH=${GIT_HASH::7} -t billreader .
