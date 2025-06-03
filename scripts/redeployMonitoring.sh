#!/bin/bash

kubectl rollout restart deployment prometheus-server -n monitoring
kubectl rollout restart deployment grafana -n monitoring
