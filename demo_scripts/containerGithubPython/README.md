# Create a Linux VM On Azure


# Login to Azure using the CLI

In order to run commands against Azure using the CLI you need to login. This is done, very simply, though the `az login` command:

FIXME: `az login` is broken in SimDem at this point run the following command and rerun this tutorial.

`
az login --scope https://management.core.windows.net//.default
`
# Install Azure CLI Extension
```
az extension add --name containerapp
```

# Register Resource Providers
```
az provider register --namespace Microsoft.App --wait

az provider register --namespace Microsoft.OperationalInsights --wait
```
# Create a resource group

A resource group is a container for related resources. All resources must be placed in a resource group. We will create one for this tutorial. 

This command used two environment variables, `RESOURCE_GROUP` is the name of the resource group and will be commonly using in other commands. `LOCATION` is the data center that the resource group will be created in. When this command has completed it will return a JSON file. You can see what the values are set at for this tutorial in that output.

```
az group create --name $RESOURCE_GROUP --location $LOCATION
```

# Create Azure Container Apps Environment
az containerapp env create --name $CONTAINERAPPS_ENVIRONMENT --resource-group $RESOURCE_GROUP --location $LOCATION

# Create Container App with a Public Image

az containerapp create --name $CONTAINER_APP_NAME --resource-group $RESOURCE_GROUP --environment $CONTAINERAPPS_ENVIRONMENT --image "$CONTAINER_IMAGE" --target-port 80 --ingress 'external'

# Test Container App with curl

CONTAINERAPP_FQDN=$(az containerapp show --resource-group $RESOURCE_GROUP --name $CONTAINER_APP_NAME --query 'properties.configuration.ingress.fqdn' --out tsv)

echo "https://${CONTAINERAPP_FQDN}"

curl "https://${CONTAINERAPP_FQDN}"

# Delete Resource Group

```
az group delete --name $RESOURCE_GROUP --yes
```
# Done!

Success! You now have scccessfully created a Container Apps image in Azure.

