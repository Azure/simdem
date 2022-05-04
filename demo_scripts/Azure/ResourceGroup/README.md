# Resource Groups

A resource group is a container for related resources. All resources must be placed in a resource group. We will create one for this tutorial. 

## Prerequisites

When working with resource groups we will need to define a resource group name, which needs to be unique within the subscription and a location for the resource group to be placed.

```
echo $MY_RESOURCE_GROUP_NAME
```

```
echo $MY_LOCATION
```

## Create the Resource Group

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
