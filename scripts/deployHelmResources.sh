#!/bin/bash

helm install vets-db-mysql bitnami/mysql --namespace spring-petclinic --version 9.3.0 --set auth.database=service_instance_db
helm install visits-db-mysql bitnami/mysql --namespace spring-petclinic  --version 9.3.0 --set auth.database=service_instance_db
helm install customers-db-mysql bitnami/mysql --namespace spring-petclinic  --version 9.3.0 --set auth.database=service_instance_db
helm install appointments-db-mysql bitnami/mysql --namespace spring-petclinic --version 9.3.0 --set auth.database=service_instance_db

helm install grafana grafana/grafana --namespace monitoring
