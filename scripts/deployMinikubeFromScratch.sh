#!/bin/bash

minikube start --driver=docker --cpus=4 --memory=4096m

kubectl apply -f k8s/init-namespace

kubectl apply -f k8s/init-services

kubectl apply -f k8s/prometheus

./scripts/deployToKubernetes.sh

./scripts/deployHelmResources.sh

echo "Grafana login: username: admin, password:" 
kubectl get secret --namespace monitoring grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo

./scripts/exposeGrafana.sh
