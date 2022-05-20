## Create Resource Group

```
export RESOURCE_GROUP_NAME=$RESOURCE_GROUP_NAME$RANDOM
```

```
az group create --location westus --name $RESOURCE_GROUP_NAME
```

Results:

```expected_similarity=0.5
{
  "id": "/subscriptions/bb318642-28fd-482d-8d07-79182df07999/resourceGroups/testResourceGroup12345",
  "location": "westus",
  "managedBy": null,
  "name": "deleteme",
  "properties": {
    "provisioningState": "Succeeded"
  },
  "tags": null,
  "type": "Microsoft.Resources/resourceGroups"
}
```

Clean up resources 
```
az group delete --name $RESOURCE_GROUP_NAME --no-wait --yes
```