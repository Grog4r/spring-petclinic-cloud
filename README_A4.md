# Setup

```bash
# Starts Minikube cluster, Creates namespaces, services, deployments and DBs
./scripts/deployMinikubeFromScratch.sh

# Expose petclinic port
minikube tunnel

# In new shell, EXTERNAL-IP is the IP of the petclinic
kubectl get svc api-gateway -n spring-petclinic
```

# Other scripts

```bash
# Expose the Grafana Frontend
./scripts/exposeGrafana.sh

# Expose the Prometheus Frontend
./scripts/exposePrometheus.sh

# Redeploy all Services in the spring-petclinic Namespace
./scripts/redeployServices.sh
```
