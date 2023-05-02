# Create a Container App On Azure
Azure Container Apps enables you to run microservices and containerized applications on a serverless platform. 
Common use cases include: Deploying API endpoints, Hosting background processing applications and more.

# Azure CLI Login
First we need to check you are logged in to the Azure in the CLI. The following command will check to see if you are logged in. 
If not it will open a browser and take you through the login steps.

To Login to Az CLI and select a subscription 
`az login` followed by `az account list --output table` and `az account set --subscription "name of subscription to use"`

To Install Az CLI
If you need to install Azure CLI run the following command: curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Prerequisites

Before you can begin you need to follow the prerequisite steps found here

1. Visit https://github.com/asw101/python-fastapi-pypy
2. Click "Use this template"
3. Name your repo "serverless-python". 
    * **If your GitHub repository Private rather than Public in step 3, you will need to click on "Package settings" on the right hand side, scroll down and click "Change visibility" button to make your package public.**
4. Create a new branch called release
5. Click on the Actions tab
6. View the output of the action
7. Return to the main repo (Code tab)
8. Click on "serverless-python" under "Packages" on the right hand side
9. Copy the `docker pull` command which will include the image name
10. Update the `GITHUB_USERNAME` environment variable below with your GitHub username or organization name.
    * **Press `b` and run the command `GITHUB_USERNAME="username"` to set variable.**
```
echo $GITHUB_USERNAME
```

# Step 1 - Install Azure CLI Extension
The Azure CLI offers the capability to load extensions. 
Extensions allow you gain access to experimental and pre-release commands.

Currently, Container App is in preview so it requries an extension.
```
az extension add --name containerapp
```

# Step 2 - Register Resource Providers
Resources are manageable items available through Azure like virtual machines or storage accounts. Resource providers supply Azure resources. 
Microsoft.App is a resource provider for Contianer Apps.
Microsoft.OperationalInsights is a resource for Azure Monitor.

The `--wait` parameter delays the next instruction until the command is completed.
```
az provider register --namespace Microsoft.App --wait
```
```
az provider register --namespace Microsoft.OperationalInsights --wait
```

# Step 3 - Create a resource group
A resource group is a container for related resources. All resources must be placed in a resource group. We will create one for this tutorial. 

This command uses two environment variables, `RESOURCE_GROUP` is the name of the resource group and will be commonly using in other commands.
`LOCATION` is the data center that the resource group will be created in. 
When this command has completed it will return a JSON file. 

You can see what the variables are set at for this tutorial in that output.
If you want to change them press `b` and run the command export `VARIABLE_NAME="new variable value"`
```
echo $LOCATION
```
```
echo $RESOURCE_GROUP
```
```
az group create --name $RESOURCE_GROUP --location $LOCATION
```

# Step 4 - Create Azure Container Apps Environment
Individual container apps are deployed to a single Container Apps environment, which acts as a secure boundary around groups of container apps.
Container Apps in the same environment are deployed in the same virtual network and write logs to the same Log Analytics workspace. 
This next command will create a Container App Environment in the Resource Group created in `Step 3`.

**Command will take ~3 minutes to complete.**

You can see what the variables are set at for this tutorial in that output.
If you want to change them press `b` and run the command export `VARIABLE_NAME="new variable value"`
```
echo $CONTAINERAPPS_ENVIRONMENT
```
```
az containerapp env create --name $CONTAINERAPPS_ENVIRONMENT --resource-group $RESOURCE_GROUP --location $LOCATION
```

# Step 5 - Create Container App with a Public Image
Now that you have an environment created, you can deploy your first container app. 
With the containerapp create command, deploy a container image to Azure Container Apps.
*NOTE: Make sure the value for the --image parameter is in lower case.*
By setting `--ingress` to external, you make the container app available to public requests.

**Command will take ~3 minutes to complete.**

You can see what the variables are set at for this tutorial in that output.
If you want to change them press `b` and run the command export `VARIABLE_NAME="new variable value"`
```
echo $GITHUB_USERNAME
```
```
CONTAINER_IMAGE=ghcr.io/$GITHUB_USERNAME/serverless-python:release
```
```
echo $CONTAINER_APP_NAME
```
```
echo $CONTAINER_IMAGE
```
```
az containerapp create --name $CONTAINER_APP_NAME --resource-group $RESOURCE_GROUP --environment $CONTAINERAPPS_ENVIRONMENT --image "$CONTAINER_IMAGE" --target-port 80 --ingress 'external'
```

# Step 6 - Test Container App with curl
The `az containerapp show` command returns the fully qualified domain name of a container app.
In the next command we are setting the domain name to the variable `CONTAINERAPP_FQDN`
```
CONTAINERAPP_FQDN=$(az containerapp show --resource-group $RESOURCE_GROUP --name $CONTAINER_APP_NAME --query "properties.configuration.ingress.fqdn" --out tsv)
```
```
echo "https://$CONTAINERAPP_FQDN"
```
```
curl "https://$CONTAINERAPP_FQDN"
```

# Success! You now have scccessfully created a Container Apps image in Azure. 
If you would like to delete the resources created push any button.
If you want to keep the resources created, push `b` and `CTRL + C` to exit the program.

# Step 7 - Delete Resource Group
The Container App and Container App Environment will be deleted with command below.

```
az group delete --name $RESOURCE_GROUP --yes
```