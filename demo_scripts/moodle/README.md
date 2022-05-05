# Deploy a scalable Moodle stack on Azure

A pre-requisite to going through this tutorial is `az login`. Please run `az login` from the command line and get back to this deployment tutorial. Many commands in this deployment experience require you to specifiy values. In order to get going as quickly as possible we've provided defaults for you.

Here are the defaults that will be used:
```
env | grep MOO
```
# Creating a local workspace for Moodle ARM and other configuration files
```
mkdir -p $MOODLE_AZURE_WORKSPACE/$MOODLE_RG_NAME
```
# We will use SSH to access infrastructure post-deployment and the following command will create a Secure Shell (SSH) key-pair to assist for when you're ready to remotely connect to your Moodle deployment via SSH
```
if [ ! -f "$MOODLE_SSH_KEY_FILENAME" ]; then ssh-keygen -t rsa -N "" -f $MOODLE_SSH_KEY_FILENAME; fi
```

# Grab the public part of the SSH key-pair to add to our configuration: this will help with remote connectivity later on
```
export SSH_PUBLIC_KEY=$(cat $MOODLE_SSH_KEY_FILENAME.pub)
```

# Verify public key string before writing to the deployment configuration parameters
```
echo $SSH_PUBLIC_KEY
```

# The next step is to clone the Moodle repository locally. The cloned files will be the blueprints for our deployments
```
git clone https://github.com/Azure/Moodle.git $MOODLE_AZURE_WORKSPACE/arm_template
```

# Verify that the directory structure and file contents are as expected before proceeding:
```
ls $MOODLE_AZURE_WORKSPACE/arm_template
```

# Write public key to Azure deployment parameter list
```
sed "s|GEN-SSH-PUB-KEY|$SSH_PUBLIC_KEY|g" $MOODLE_AZURE_WORKSPACE/arm_template/azuredeploy.parameters.json > $MOODLE_AZURE_WORKSPACE/$MOODLE_RG_NAME/azuredeploy.parameters.json
```

# Now it's time to start deploying Azure infrastructure: let's begin with a Resource Group
```
az group create --name $MOODLE_RG_NAME --location $MOODLE_RG_LOCATION
```

Results:

```expected_similarity=0.3
  "id": "/subscriptions/325e7c34-99fb-4190-aa87-1df746c67705/resourceGroups/simdemMoodleRG",
  "location": "eastus",
  "managedBy": null,
  "name": "simdemMoodleRG",
  "properties": {
    "provisioningState": "Succeeded"
  },
  "tags": null,
  "type": "Microsoft.Resources/resourceGroups"
```

# Finally, let's kick off the deployment for Moodle. This will take some time; sometimes up to an hour. Now would be a good time to get catch up on other work and come back here in a bit!
```
az deployment group create --name $MOODLE_DEPLOYMENT_NAME --resource-group $MOODLE_RG_NAME --template-file $MOODLE_AZURE_WORKSPACE/arm_template/azuredeploy.json --parameters $MOODLE_AZURE_WORKSPACE/$MOODLE_RG_NAME/azuredeploy.parameters.json
```

# Done!
That's it! You now have a scalable Moodle deployment running in Azure. 

# Next Steps
  1. [Delete all resources](Cleanup.md)

