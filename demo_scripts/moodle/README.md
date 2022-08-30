# Tutorial: Deploy a Scalable Moodle stack on Azure

## Prerequisites
 - Create an Azure [Resource Group](../Azure/ResourceGroup/README.md)
 - Access to Azure CLI with an active subscription. To install Azure CLI see https://docs.microsoft.com/en-us/cli/azure/install-azure-cli.
 - If you have multiple Azure subscriptions, select the appropriate subscription ID in which the resources should be billed using the az account command.
 - This tutorial requires version 2.0.64 or later of the Azure CLI. If using Azure Cloud Shell, the latest version is already installed.
 - If you're using a local installation, sign in to the Azure CLI by using the az login command. To finish the authentication process, follow the steps displayed in your terminal. For other sign-in options, see Sign in with the Azure CLI.
 
 ## Setup
 Many commands in this deployment experience require you to specify values. In order to get going as quickly as possible we've provided defaults for you.

Here are the defaults that will be used:
```bash
env | grep MY
```
# Creating a local workspace 

The first step is to create a workspace for Moodle, ARM, and other configuration files
```bash
mkdir -p $MY_AZURE_WORKSPACE/$MY_RESOURCE_GROUP_NAME
```
# Set up SSH Keys
1. We will use SSH to access infrastructure post-deployment and the following command will create a Secure Shell (SSH) key-pair to assist for when you're ready to remotely connect to your Moodle deployment via SSH
```bash
if [ ! -f "$MY_SSH_KEY_FILENAME" ]; then ssh-keygen -t rsa -N "" -f $MY_SSH_KEY_FILENAME; fi
```

2. Store the public portion of the SSH key-pair as an environment variable. This will help with remote connectivity in a future step.
```bash
export SSH_PUBLIC_KEY=$(cat $MY_SSH_KEY_FILENAME.pub)
```

3. Validate SSH Key value public key string exists before writing to the deployment configuration parameters
```bash
echo $SSH_PUBLIC_KEY
```

Results:
```expected_similarity=0.015
ssh-rsa abcdefghijklmnopqrstuvwxyznabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcd/zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz/abcdefghijklmnopqrstuvwxyznabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdabcdefghijklmnopqrstuvwxyzaabcdefghijklmnopqrstuvwxyznabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcd+abcdefghijklmnopqrstuvwxyznabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijkl= root@localhost
```

# Clone Moodle Repository Locally 

The next step is to clone the Moodle repository locally. The cloned files will be the blueprints for our deployments
```bash
git clone https://github.com/Azure/Moodle.git $MY_AZURE_WORKSPACE/arm_template
```

# Verify that the directory structure and file contents are as expected before proceeding:
```bash
ls $MY_AZURE_WORKSPACE/arm_template
```
Results:
```expected_similarity=0.5
CONTRIBUTE.md              azuredeploy-small2mid-noha.json  managedApplication
Gruntfile.js               azuredeploy.json                 metadata.json
LICENSE                    azuredeploy.parameters.json      migration
LICENSE-DOCS               docs                             nested
README.md                  env.json                         package.json
azuredeploy-large-ha.json  etc                              scripts
azuredeploy-maximal.json   images
azuredeploy-minimal.json   loadtest
```

# Write public key to Azure deployment parameter list
```bash
sed "s|GEN-SSH-PUB-KEY|$SSH_PUBLIC_KEY|g" $MY_AZURE_WORKSPACE/arm_template/azuredeploy.parameters.json > $MY_AZURE_WORKSPACE/$MY_RESOURCE_GROUP_NAME/azuredeploy.parameters.json
```

# Deploy Moodle Resources to Azure 
Finally, let's kick off the deployment for Moodle. This will take some time; sometimes up to an hour. Now would be a good time to get catch up on other work and come back here in a bit!
```bash
az deployment group create --name $MY_DEPLOYMENT_NAME --resource-group $MY_RESOURCE_GROUP_NAME --template-file $MY_AZURE_WORKSPACE/arm_template/azuredeploy.json --parameters $MY_AZURE_WORKSPACE/$MY_RESOURCE_GROUP_NAME/azuredeploy.parameters.json
```
 
## Check that your deployment is accessible 
Now that the Moodle deployment is complete, we can reach the public endpoint. The following commands will show the fully qualified domain name which you can use to access your Moodle instance.c

Obtain the FQDN with the following: 
```bash
az network public-ip show --resource-group $MY_RESOURCE_GROUP_NAME --name $(az network public-ip list -o table --query [].name | grep lb-pubip) --query dnsSettings.fqdn
```

# Done!
That's it! You now have a scalable Moodle deployment running in Azure.


