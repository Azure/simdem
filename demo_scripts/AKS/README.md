# Create a Cluster

You can't do anything until you ahve an AKS cluster to work with, so lets do that first.

## Prerequisites

First we need to check you are logged in to the Azure in the CLI. The following command will check to see if you are logged in. If not it will open a browser and take you through the login steps.

`
az login
`

## Create a resource group

A resource group is a container for related resources. All resources must be placed in a resource group. We will create one for this tutorial. 

This command used two environment variables, `MY_RESOURCE_GROUP_NAME` is the name of the resource group and will be commonly using in other commands. `MY_LOCATION` is the data center that the resource group will be created in. When this command has completed it will return a JSON file. You can see what the values are set at for this tutorial in that output.

```
az group create --name $MY_RESOURCE_GROUP_NAME --location $MY_LOCATION
```

Results:

```expected_similarity=0.3
  "id": "/subscriptions/325e7c34-99fb-4190-aa87-1df746c67705/resourceGroups/myResourceGroup",
  "location": "eastus",
  "managedBy": null,
  "name": "myResourceGroup",
  "properties": {
    "provisioningState": "Succeeded"
  },
  "tags": null,
  "type": "Microsoft.Resources/resourceGroups"
```

## Create an AKS Cluster

Create an AKS cluster using the az aks create command with the --enable-addons monitoring parameter to enable Azure Monitor container insights. The following example creates a cluster named myAKSCluster with one node:

```
az aks create --resource-group $MY_RESOURCE_GROUP_NAME --name $MY_AKS_CLUSTER_NAME --node-count 1 --enable-addons monitoring --generate-ssh-keys
```

Results:

```expected_similarity=0.3

```

## Connect to the Cluster

To manage a Kubernetes cluster you need Kubectl installed. The following command will install it for you if necessary.

`
sudo az aks install-cli
`

Results:

```expected_similarity=0.3
Downloading client to "/usr/local/bin/kubectl" from "https://storage.googleapis.com/kubernetes-release/release/v1.23.5/bin/linux/amd64/kubectl"
Please ensure that /usr/local/bin is in your search PATH, so the `kubectl` command can be found.
Downloading client to "/tmp/tmpl2lbjmrj/kubelogin.zip" from "https://github.com/Azure/kubelogin/releases/download/v0.0.12/kubelogin.zip"
Please ensure that /usr/local/bin is in your search PATH, so the `kubelogin` command can be found.
```

Setup the credentials for accessing the cluster via Kubectl:

```
az aks get-credentials --resource-group $MY_RESOURCE_GROUP_NAME --name $MY_AKS_CLUSTER_NAME --overwrite-existing
```
Results:

```expected_similarity=0.3
Merged "myAKSCluster" as current context in /home/username/.kube/config
```

Verify connectivity via Kubectl:

```
kubectl get nodes
```

Results:

```expected_similarity=0.3
NAME                                STATUS   ROLES   AGE   VERSION
aks-nodepool1-33734636-vmss000000   Ready    agent   05m   v1.22.6
```

# Next Steps

You now have a cluster up and running, but you do not have an applicationd deployed. What would you like to do next?

  1. [Deploy an Application](AppDeployment/README.md)