#!/bin/bash
sudo docker stop fast_api_app
sudo docker rm fast_api_app
sudo docker build -t my_project .
sudo docker run -d --name fast_api_app --log-driver=json-file -p 4441:8000 my_project
