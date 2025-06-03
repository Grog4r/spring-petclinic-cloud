#!/bin/bash

helm install vets-db-mysql bitnami/mysql --namespace spring-petclinic --version 9.3.0 --set auth.database=service_instance_db
helm install visits-db-mysql bitnami/mysql --namespace spring-petclinic  --version 9.3.0 --set auth.database=service_instance_db
helm install customers-db-mysql bitnami/mysql --namespace spring-petclinic  --version 9.3.0 --set auth.database=service_instance_db
helm install appointments-db-mysql bitnami/mysql --namespace spring-petclinic --version 9.3.0 --set auth.database=service_instance_db

kubectl create configmap grafana-datasources \
  --from-file=datasources.yaml=./k8s/grafana-config/datasources.yaml \
  -n monitoring

kubectl create configmap grafana-dashboard-provider \
  --from-file=dashboard-provider.yaml=./k8s/grafana-config/dashboard-provider.yaml \
  -n monitoring

kubectl create configmap grafana-dashboards \
  --from-file=spring-petclinic-dashboard.json=./k8s/grafana-config/dashboards/grafana-petclinic-dashboard.json \
  -n monitoring

# helm install grafana grafana/grafana --namespace monitoring

helm upgrade --install grafana grafana/grafana \
  --namespace monitoring \
  --set persistence.enabled=true \
  --set adminPassword='admin' \
  --set sidecar.datasources.enabled=false \
  --set sidecar.dashboards.enabled=false \
  --set grafana.ini.dashboard.providers.path=/etc/grafana/provisioning/dashboards \
  --set grafana.ini.datasources.path=/etc/grafana/provisioning/datasources \
  --set extraConfigmapMounts[0].name=grafana-datasources \
  --set extraConfigmapMounts[0].mountPath=/etc/grafana/provisioning/datasources \
  --set extraConfigmapMounts[0].configMap=grafana-datasources \
  --set extraConfigmapMounts[0].readOnly=true \
  --set extraConfigmapMounts[1].name=grafana-dashboard-provider \
  --set extraConfigmapMounts[1].mountPath=/etc/grafana/provisioning/dashboards \
  --set extraConfigmapMounts[1].configMap=grafana-dashboard-provider \
  --set extraConfigmapMounts[1].readOnly=true \
  --set extraConfigmapMounts[2].name=grafana-dashboards \
  --set extraConfigmapMounts[2].mountPath=/var/lib/grafana/dashboards \
  --set extraConfigmapMounts[2].configMap=grafana-dashboards \
  --set extraConfigmapMounts[2].readOnly=true
