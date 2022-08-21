## Create a Resource Group
An Azure resource group is a logical group in which Azure resources are deployed and managed. When you create a resource group, you are prompted to specify a location. This location is:
  - The storage location of your resource group metadata.
  - Where your resources will run in Azure if you don't specify another region during resource creation.

Validate specified Resource Group does not already exist. If it does, select a new Resource Group name by running the following:

```
if [ "$(az group exists --name $RESOURCE_GROUP_NAME)" = 'true' ]; then export RAND=$RANDOM; export RESOURCE_GROUP_NAME="$RESOURCE_GROUP_NAME$RAND"; echo "Your new Resource Group Name is $RESOURCE_GROUP_NAME"; fi
```

Create a Resource Group using the "az group create" command:
```
az group create --name $RESOURCE_GROUP_NAME --location $RESOURCE_LOCATION
```


##Create Azure Container Registry

Azure Container Registry allows you to build, store, and manage container images and artifacts in a private registry for all types of container deployments.
The registry name must be unique within Azure, and contain 5-50 lowercase alphanumeric characters. 
The following command uses a random string to ensure the Azure Container is given a unique name. 
```
export RAND=$RANDOM; export RAND=$RANDOM export MYACR="$RAND$MYACR$RAND"; echo "Your new Resource Group Name is $MYACR"; 
```

# Run the following line to create an Azure Container Registry 
This may take a few minutes
```
az acr create -n $MYACR -g $RESOURCE_GROUP_NAME --sku basic
```

## Create an AKS cluster with ACR integration

You can set up AKS and ACR integration during the initial creation of your AKS cluster. 
To allow an AKS cluster to interact with ACR, an Azure Active Directory managed identity is used. 
The following command configures the appropriate ACRPull role for the managed identity.


The following example creates a cluster named myAKSCluster, integrated with the Azure Container Registry created in the previous step.
Create an AKS cluster using the az aks create command. This will take a few minutes.

```
az aks create -n $AKS_CLUSTER_NAME -g  $RESOURCE_GROUP_NAME --generate-ssh-keys --attach-acr $MYACR
```
## Connect to the cluster
To manage a Kubernetes cluster, use the Kubernetes command-line client, kubectl. kubectl is already installed if you use Azure Cloud Shell. 
1. Install az aks CLI locally using the az aks install-cli command

```
if ! [ -x "$(command -v kubectl)" ]; then az aks install-cli; fi
```

2. Configure kubectl to connect to your Kubernetes cluster using the az aks get-credentials command. The following command:
    - Downloads credentials and configures the Kubernetes CLI to use them.
    - Uses ~/.kube/config, the default location for the Kubernetes configuration file. Specify a different location for your Kubernetes configuration file using --file argument. 

> [!WARNING]
> This will overwrite any existing credentials with the same entry

```
az aks get-credentials --resource-group $RESOURCE_GROUP_NAME --name $AKS_CLUSTER_NAME --overwrite-existing
```

3. Verify the connection to your cluster using the kubectl get command. This command returns a list of the cluster nodes. For this tutorial you should have 3.  

```
kubectl get nodes
```


##Basic NGINX ingress controller 
An Ingress controller is a specialized load balancer for Kubernetes (and other containerized) environments. Kubernetes ingress resources are used to configure the ingress rules and routes for individual Kubernetes services.

This tutorial uses Helm 3 to install the NGINX ingress controller on a supported version of Kubernetes.
The following commands create a basic NGINX ingress controller without customizing the defaults
```
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update
helm install ingress-nginx ingress-nginx/ingress-nginx --create-namespace --namespace $NAMESPACE  --set controller.service.annotations."service\.beta\.kubernetes\.io/azure-load-balancer-health-probe-request-path"=/healthz
```



## Varnish Secret 
A Secret is an object that contains a small amount of sensitive data such as a password, a token, or a key. Such information might otherwise be put in a Pod specification or in a container image. 
Using a Secret means that you don't need to include confidential data in your application code. Learn more at: https://kubernetes.io/docs/concepts/configuration/secret/

Here we create a secret for Varnish cli admin operations:
``` 
kubectl create secret generic varnish-secret --from-literal=secret=$(head -c32 /dev/urandom  | base64)
```

## Varnish VCL config 
We use the default.vcl file to create a config map A ConfigMap allows you to decouple environment-specific configuration from your container images, 
so that your applications are easily portable. Learn more at: https://kubernetes.io/docs/concepts/configuration/configmap/
```
kubectl create configmap varnish-vcl --from-file=default.vcl
```

The backend definition in the VCL file refers to the origin server for which we are caching HTTP resources.  
The .host property contains the hostname of the origin and the .port property contains the port number on which your origin is listening for incoming HTTP connections.
More information at https://www.varnish-software.com/developers/tutorials/running-varnish-docker/

We are using the internal IP address 10.224.0.42 here. Feel free to use any available private IP addresses in virtual network.
```
cat default.vcl 
```

Set the namespace to ingress-basic 
```
 kubectl config set-context --current --namespace=ingress-basic
 ```

1. To deploy the application apply the following command: 
This will deploy the demo Azure Voting application that we wll use as a backend for our varnish cache.
We do this with a manifest to create all objects needed to run the Azure Vote application. 
                -Information about this deployment can be found: https://docs.microsoft.com/en-us/azure/aks/learn/quick-kubernetes-deploy-cli
                
Note this command may result in a "warning" based on the NGINX ingress controller we are using, for our purposes we can ignore the warning and continue. 
```
 kubectl apply -f  demo-application.yaml
```
2. This will also deploy the varnish cache that uses the demo application as a backend. 
We do this with a manifest file that creates Varnish service and Varnish proxy pods. 
                -Information about this deployment can be found here: https://kruyt.org/varnish-kuberenets/#:~:text=%20Varnish%20in%20Kubernetes%20%201%20Setup.%20Apply,to%20the%20varnish%20service.%20Multiple%20ingresses...%20More%20
```
 kubectl apply -f  varnish.yaml
```
3. This will deploy the ingress resource that is responsible for routing the traffic to the Varnish Cache. 
                 -Information about this deployment can be found here: https://docs.microsoft.com/en-us/azure/aks/ingress-basic?tabs=azure-cli

```
 kubectl apply -f  varnish-ingress.yaml 
```


Run the Following command to get the Public IP address: 
```
 kubectl get svc
 ```


The following command captures the IP address and stores it in an environment variable.
```
MY_APP_IP=$(kubectl get service ingress-nginx-controller -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
 ```

 ```
 echo " Your IP address is: $MY_APP_IP ! Try it out in the browser"
 ```
Congratulations! You've successfully deployed a scalable Varnish cluster to Azure Kubernetes Service. In the process, you created a Resource group, an Azure Container Registry,
 an AKS cluster with ACR integration, and an ingress controller. To the Kubernetes cluster, you deployed the demo voting app, ingress resource, and a scalable Varnish cache!
 The only next steps are to clean up deployed Azure resources with the following commands

##Clean up Resources 
This tutorial used Helm to install the ingress components and demo voting app. When you deploy a Helm chart, many Kubernetes resources are created. 
These resources include pods, deployments, and services. To clean up these resources, you can either delete the entire sample namespace, or the individual resources.


To delete the entire sample namespace, use the kubectl delete command and specify your namespace name. All the resources in the namespace are deleted.
This may take a few minutes. 
```
kubectl delete namespace ingress-basic
 ```

Use the az group delete command to remove the resource group, cluster, and container service to avoid unnecessary charges. 
This will take a few minutes. 
```
az group delete --name $RESOURCE_GROUP_NAME --yes
```