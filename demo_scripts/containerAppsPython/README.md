# Create a Container App On Azure
Azure Container Apps enables you to run microservices and containerized applications on a serverless platform. 

# Prerequisites

First we need to check you are logged in to the Azure in the CLI. The following command will check to see if you are logged in. If not it will open a browser and take you through the login steps. 

FIXME az login --scope https://management.core.windows.net//.default

```
echo $LOCATION
echo $RESOURCE_GROUP
az group create --name $RESOURCE_GROUP --location $LOCATION
```
# az group delete --name $RESOURCE_GROUP --yes


# Step 1 - Install Azure CLI Extension

The Azure CLI offers the capability to load extensions. 
Extensions allow you gain access to experimental and pre-release commands.
Currently, Container App is in preview.

```
az extension add --name containerapp
```

# Step 2 - Register Resource Providers
Resources are manageable items available through Azure like virtual machines or storage accounts.
Resource providers supply Azure resources. 
Microsoft.App is a resource provider for Contianer Apps.
Microsoft.OperationalInsights is a resource for Azure Monitor.
The `--wait` delays the next instruction until the command is completed.

```
az provider register --namespace Microsoft.App --wait

az provider register --namespace Microsoft.OperationalInsights --wait
```
# Step 3 - Create a resource group

A resource group is a container for related resources. All resources must be placed in a resource group. We will create one for this tutorial. 

This command uses two environment variables, `RESOURCE_GROUP` is the name of the resource group and will be commonly using in other commands. `LOCATION` is the data center that the resource group will be created in. When this command has completed it will return a JSON file. You can see what the values are set at for this tutorial in that output.

```
echo $LOCATION
echo $RESOURCE_GROUP
az group create --name $RESOURCE_GROUP --location $LOCATION
```

# Step 4 - Create Azure Container Apps Environment
```
az containerapp env create --name $CONTAINERAPPS_ENVIRONMENT --resource-group $RESOURCE_GROUP --location $LOCATION
```
# Step 5 - Create Container App with a Public Image


By setting `--ingress` to external, you make the container app available to public requests.
```
az containerapp create --name $CONTAINER_APP_NAME --resource-group $RESOURCE_GROUP --environment $CONTAINERAPPS_ENVIRONMENT --image "$CONTAINER_IMAGE" --target-port 80 --ingress 'external'
```
# Step 6 - Test Container App with curl

CONTAINERAPP_FQDN=$(az containerapp show --resource-group $RESOURCE_GROUP --name $CONTAINER_APP_NAME --query 'properties.configuration.ingress.fqdn' --out tsv)
```
echo "https://${CONTAINERAPP_FQDN}"

curl "https://${CONTAINERAPP_FQDN}"
```
# Step 7 - Delete Resource Group

```
az group delete --name $RESOURCE_GROUP --yes
```
# Done!

Success! You now have scccessfully created a Container Apps image in Azure.

