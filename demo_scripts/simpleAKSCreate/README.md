# Quickstart: Deploy Azure Kubernetes Service cluster & Web App using the Azure CLI
Welcome to this tutorial where we will take you step by step in creating an Azure Kubernetes Web Application. This tutorial assumes you are logged into Azure CLI already and have selected a subscription to use with the CLI. It also assumes that you have Helm installed (Instructions can be found here https://helm.sh/docs/intro/install/). If you are using Azure cloud shell all of these requirements are already met.

To Login to Az CLI and select a subscription 
'az login' followed by 'az account list --output table' and 'az account set --subscription "name of subscription to use"'

To Install Az CLI
If you need to install Azure CLI run the following command - curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash


## Define Command Line Variables 
The first step is to define command line variables to reference in the deployment. 

```bash
export RESOURCE_GROUP_NAME=myResourceGroup
export RESOURCE_LOCATION=eastus
export AKS_CLUSTER_NAME=myAKSCluster
export PUBLIC_IP_NAME=myPublicIp
export VNET_NAME=myVnet
export SUBNET_NAME=mySubnet
export APPLICATION_GATEWAY_NAME=myAKSCluster
```

## Create A Resource Group
An Azure resource group is a logical group in which Azure resources are deployed and managed. When you create a resource group, you are prompted to specify a location. This location is:
  - The storage location of your resource group metadata.
  - Where your resources will run in Azure if you don't specify another region during resource creation.

Validate Resource Group does not already exist. If it does, select a new resource group name by running the following:

```bash
if [ "$(az group exists --name $RESOURCE_GROUP_NAME)" = 'true' ]; then export RAND=$RANDOM; export RESOURCE_GROUP_NAME="$RESOURCE_GROUP_NAME$RAND"; echo "Your new Resource Group Name is $RESOURCE_GROUP_NAME"; fi
```

Create a resource group using the az group create command:
```bash
az group create --name $RESOURCE_GROUP_NAME --location $RESOURCE_LOCATION
```
Results:

```expected_similarity=0.5
{
  "id": "/subscriptions/bb318642-28fd-482d-8d07-79182df07999/resourceGroups/testResourceGroup24763",
  "location": "eastus",
  "managedBy": null,
  "name": "testResourceGroup",
  "properties": {
    "provisioningState": "Succeeded"
  },
  "tags": null,
  "type": "Microsoft.Resources/resourceGroups"
}
```

## Register to AKS Azure Resource Providers
Verify Microsoft.OperationsManagement and Microsoft.OperationalInsights providers are registered on your subscription. These are Azure resource providers required to support [Container insights](https://docs.microsoft.com/en-us/azure/azure-monitor/containers/container-insights-overview). To check the registration status, run the following commands

```bash
az provider register --namespace Microsoft.OperationsManagement
az provider register --namespace Microsoft.OperationalInsights
```

## Create AKS Cluster 
Create an AKS cluster using the az aks create command with the --enable-addons monitoring parameter to enable Container insights. The following example creates a cluster named myAKSCluster with one node:

This will take a few minutes
```bash
az aks create --resource-group $RESOURCE_GROUP_NAME --name $AKS_CLUSTER_NAME --node-count 1 --enable-addons monitoring --generate-ssh-keys
```

## Connect to the cluster
To manage a Kubernetes cluster, use the Kubernetes command-line client, kubectl. kubectl is already installed if you use Azure Cloud Shell.

1. Install az aks CLI locally using the az aks install-cli command

```bash
if ! [ -x "$(command -v kubectl)" ]; then az aks install-cli; fi
```

2. Configure kubectl to connect to your Kubernetes cluster using the az aks get-credentials command. The following command:
    - Downloads credentials and configures the Kubernetes CLI to use them.
    - Uses ~/.kube/config, the default location for the Kubernetes configuration file. Specify a different location for your Kubernetes configuration file using --file argument. 

> [!WARNING]
> This will overwrite any existing credentials with the same entry

```bash
az aks get-credentials --resource-group $RESOURCE_GROUP_NAME --name $AKS_CLUSTER_NAME --overwrite-existing
```

3. Verify the connection to your cluster using the kubectl get command. This command returns a list of the cluster nodes.

```bash
kubectl get nodes
```

## Deploy the Web Application 
A Kubernetes manifest file defines a cluster's desired state, such as which container images to run.

In this quickstart, you will use a manifest to create all objects needed to run the Azure Vote application. This manifest includes two Kubernetes deployments:

- The sample Azure Vote Python applications.
- A Redis instance.

Two Kubernetes Services are also created:

- An internal service for the Redis instance.
- An external service to access the Azure Vote application from the internet.

A test voting app YML file is already prepared. To deploy this app run the following command 
```bash
kubectl apply -f azure-vote-start.yml
```

## Test The Application
When the application runs, a Kubernetes service exposes the application front end to the internet. This process can take a few minutes to complete.

Check progress using the kubectl get service command.

```bash
kubectl get service
```

Store the public IP Address as an environment variable for later use.
>[!Note]
> This commmand loops for 2 minutes and queries the output of kubectl get service for the IP Address. Sometimes it can take a few seconds to propogate correctly 
```bash
runtime="2 minute"; endtime=$(date -ud "$runtime" +%s); while [[ $(date -u +%s) -le $endtime ]]; do export IP_ADDRESS=$(kubectl get service azure-vote-front --output jsonpath='{.status.loadBalancer.ingress[0].ip}'); if ! [ -z $IP_ADDRESS ]; then break; else sleep 10; fi; done
```

Run the following command to obtain the URL of the AKS Web Application

```bash
echo "http://${IP_ADDRESS}"
```

Browse your AKS Application! 

# Next Steps

Congratulations you have no created an AKS cluster with a web application. You can manage the AKS cluster in the Azure portal under the resource group myResourceGroup