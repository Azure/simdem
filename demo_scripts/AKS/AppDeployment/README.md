# Deploy An Application to AKS

A Kubernetes manifest file defines a cluster's desired state, such as which container images to run. In this quickstart, you will use a simple manifest to create all objects needed to run the Azure Vote application.

Lets take a look at the manifest we will use:

```
cat $MY_APPLICATION_YAML_PATH
```

Results:

```expected_similarity=0.3
apiVersion: apps/v1
kind: Deployment
metadata:
  name: azure-vote-back
spec:
  replicas: 1
  selector:
    matchLabels:
      app: azure-vote-back
  template:
    metadata:
      labels:
        app: azure-vote-back
    spec:
      nodeSelector:
        "kubernetes.io/os": linux
      containers:
      - name: azure-vote-back
        image: mcr.microsoft.com/oss/bitnami/redis:6.0.8
        env:
        - name: ALLOW_EMPTY_PASSWORD
          value: "yes"
        resources:
          requests:
            cpu: 100m
            memory: 128Mi
          limits:
            cpu: 250m
            memory: 256Mi
        ports:
        - containerPort: 6379
          name: redis
---
apiVersion: v1
kind: Service
metadata:
  name: azure-vote-back
spec:
  ports:
  - port: 6379
  selector:
    app: azure-vote-back
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: azure-vote-front
spec:
  replicas: 1
  selector:
    matchLabels:
      app: azure-vote-front
  template:
    metadata:
      labels:
        app: azure-vote-front
    spec:
      nodeSelector:
        "kubernetes.io/os": linux
      containers:
      - name: azure-vote-front
        image: mcr.microsoft.com/azuredocs/azure-vote-front:v1
        resources:
          requests:
            cpu: 100m
            memory: 128Mi
          limits:
            cpu: 250m
            memory: 256Mi
        ports:
        - containerPort: 80
        env:
        - name: REDIS
          value: "azure-vote-back"
---
apiVersion: v1
kind: Service
metadata:
  name: azure-vote-front
spec:
  type: LoadBalancer
  ports:
  - port: 80
  selector:
    app: azure-vote-front
```

Deploying the application is done via the standard Kubectl tool:

```
kubectl apply -f $MY_APPLICATION_YAML_PATH
```

Results:

```expected_similarity=0.3
deployment.apps/azure-vote-back created
service/azure-vote-back created
deployment.apps/azure-vote-front created
service/azure-vote-front created
```

## Test the application

When the application runs, a Kubernetes service exposes the application front end to the internet. This process can take a few minutes to complete. Using the `get service` command with a `--watch` switch allows you to monitor progress, e.g. `kubectl get service azure-vote-front --watch`. When the `EXTERNAL-IP` becomes available then you are ready to go.

However, when running in automated scripts it is helpful to capture the IP and store it in an environment varable. So lets do that:

```
export MY_APP_IP=$(kubectl get service azure-vote-front -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
```

However, usually it takes a little while for the IP to be available, so lets repeat that command until the value is set.

```
while [ -z "$MY_APP_IP" ]; do export MY_APP_IP=$(kubectl get service azure-vote-front -o jsonpath='{.status.loadBalancer.ingress[0].ip}'); done
```

Results:

```expected_similarity=0.3
NAME               TYPE           CLUSTER-IP   EXTERNAL-IP    PORT(S)        AGE
azure-vote-front   LoadBalancer   10.0.202.8   20.102.27.76   80:32736/TCP   88s
```

Now you can open the application at the provided IP in your browser.

```
xdg-open http://$MY_APP_IP
```
