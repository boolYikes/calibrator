#!/bin/bash

docker stop calibrator_box
docker rm calibrator_box
docker rmi calibrator
docker build -t calibrator .
docker run -p 5000:5000 --name calibrator_box calibrator