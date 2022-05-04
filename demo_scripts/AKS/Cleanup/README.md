# Remove all resources

This script will use the following configuration. You can change these by setting a value in the shell.

```
env | grep MY_
```

# Cleanup all resources

If you want to delete all the resources created in this script simply run the following command. Type `quit` if you want to keep them.

```
az group delete --name $MY_RESOURCE_GROUP_NAME
```

Done!
