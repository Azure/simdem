
# Azure Script Testing

Replace this file with the readme.md of the Azure scenario you would like to test. The goal is to automatically do this anytime a readme is changed, but we haven't worked out that feature yet :) 

If there are any additional files you take advantage of you can put them in this folder as well. For example, for the AKSDeployment test we require some YML files which are also placed here. 

You need to use the environment variable $RESOURCE_GROUP_NAME for any resource group that you create. This will deploy to a test resource group which is automatically deleted at the end of the process. 

Create Azure resources

```bash
echo $RESOURCE_GROUP_NAME
```

Check resource group exists

```bash
az group exists --name $RESOURCE_GROUP_NAME
```

Finished with Azure Tests for now...
