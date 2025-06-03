#!/bin/bash

echo "Connection available at http://127.0.0.1:9090"

kubectl port-forward -n monitoring svc/prometheus-service 9090:80
