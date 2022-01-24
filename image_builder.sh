#!/bin/bash

# Builds the docker image, passing the git hash as a build arg
# and the billreader package version as the tag.
# 
# Run this from the root of the package.

tag_version="$(python3 setup.py --version)"
export GIT_HASH=$(git rev-parse HEAD)
docker build --build-arg GIT_HASH=${GIT_HASH::7} -t "billreader:$tag_version" .
