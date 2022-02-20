#!/bin/bash

# Builds the docker image, passing the git hash as a build arg

cd ~/Documents/Python/bill-pdfs/
docker build -t billreader .
