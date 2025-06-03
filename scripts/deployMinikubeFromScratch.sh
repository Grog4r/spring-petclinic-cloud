#!/bin/bash

minikube start --driver=docker --cpus=4 --memory=4096m

kubectl apply -f k8s/init-namespace

kubectl apply -f k8s/init-services

kubectl apply -f k8s/prometheus

./scripts/deployToKubernetes.sh

./scripts/deployHelmResources.sh

./scripts/exposeGrafana.sh
