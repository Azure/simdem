# Run a Docker Container in Azure Container Instances (ACI)

This document will walk you through running a Docker container in Azure Container Instances.

# Prerequisites

This script uses the following environment variables:

```
env | grep MY_
```

As is nearly always the case when working with resources on Azure, you need to [create a resource group](../Azure/ResourceGroup/README.md) to deploy your resources to.

# Deploy the Container

Each ACI container that will be publicly accessible needs a DNS name. You can generate a random one with the following command:

```
MY_ACS_DNS_LABEL=$MY_CONTAINER_NAME-$RANDOM
```

A single command will now deploy your container for your:

```
az container create --resource-group $MY_RESOURCE_GROUP_NAME --name $MY_CONTAINER_NAME --image $MY_CONTAINER_IMAGE --ports 80 --dns-name-label $MY_ACS_DNS_LABEL --location $MY_LOCATION
```

# Wait for full deployment

It can take a short while for the deployment to complete you can get the status of the deployment with:

```
MY_STATUS=$(az container show --resource-group $MY_RESOURCE_GROUP_NAME --name $MY_CONTAINER_NAME --query "{FQDN:ipAddress.fqdn,ProvisioningState:provisioningState}" --output table)
```

Which is currently giving a status of:

```
echo $MY_STATUS
```

When the container is ready the provisioning state will say "Succceeded". When scripting this it may be necessary to wait until the succeeded state is reached. This can be achieved with the following loop:

```
while [[ "$MY_STATUS" != "Succeeded" ]]; do MY_STATUS=$(az container show --resource-group $MY_RESOURCE_GROUP_NAME --name $MY_CONTAINER_NAME --query "{ProvisioningState:provisioningState}" --output tsv); done
```

At this point we know the deployment has succeeded and can open a web connection to the container:

```
xdg-open http://$MY_ACS_DNS_LABEL.$MY_LOCATION.azurecontainer.io
```
