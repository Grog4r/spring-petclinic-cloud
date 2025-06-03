#!/bin/bash

kubectl rollout restart deployment customers-service -n spring-petclinic
kubectl rollout restart deployment appointments-service -n spring-petclinic
kubectl rollout restart deployment visits-service -n spring-petclinic
kubectl rollout restart deployment vets-service -n spring-petclinic
kubectl rollout restart deployment api-gateway -n spring-petclinic
