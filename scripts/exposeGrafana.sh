#!/bin/bash

kubectl expose service grafana -n monitoring --type=NodePort --target-port=3000 --name=grafana-ext

minikube service grafana-ext -n monitoring

echo "Grafana login: username: admin, password: admin"
