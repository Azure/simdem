# Create a Linux VM On Azure

Many commands in the CLI require you to specifiy values. In order to get going as quickly as possible we've provided defaults for your.
At the end of this tutorial you will have the option to download a script that will repeat all the steps for you using environment variables. By setting these environment variables and running the script you will be able to customize your VM. 

Here are the defaults that will be used. Don't worry about what they are used for, they will be explained as they become important.

The environment now is:

```
env | grep MY_
```

# Login to Azure using the CLI

In order to run commands against Azure using the CLI you need to login. This is done, very simply, though the `az login` command:

FIXME: `az login` is broken in SimDem at this point run the following command and rerun this tutorial.

`
az login --scope https://management.core.windows.net//.default
`

# Create a resource group

A resource group is a container for related resources. All resources must be placed in a resource group. We will create one for this tutorial. 

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

# Create the Virtual Machine

To create a VM in this resource group we need to run a simple command, here we have provided the `--generate-ssh-keys` flag, this will cause the CLI to look for an avialable ssh key in `~/.ssh`, if one is found it will be used, otherwise one will be generated and stored in `~/.ssh`. We also provide the `--public-ip-sku Standard` flag to ensure that the machine is accessible via a public IP. Finally, we are deploying an `UbuntuLTS` image. 

All other values are configured using environment variables.

```
az vm create --resource-group $MY_RESOURCE_GROUP_NAME --name $MY_VM_NAME --image UbuntuLTS --admin-username $MY_USERNAME --generate-ssh-keys --public-ip-sku Standard
```

Results:

```expected_similarity=0.3
  "fqdns": "",
  "id": "/subscriptions/325e7c34-99fb-4190-aa87-1df746c67705/resourceGroups/myResourceGroup/providers/Microsoft.Compute/virtualMachines/myVM",
  "location": "eastus",
  "macAddress": "00-0D-3A-10-4F-70",
  "powerState": "VM running",
  "privateIpAddress": "10.0.0.4",
  "publicIpAddress": "52.147.208.85",
  "resourceGroup": "myResourceGroup",
  "zones": ""
```

# Done!

That's it! You now have a VM running in Azure. The output above provides details about how to connect to the VM. You can manage it through the CLI or through the portal.

# Next Steps

  1. [Install a web server and connect via a browser](WebSever.md)
  2. [Install a Go development environment and SSH in](GoDevelopment.md)
  3. [Delete all resources](Cleanup/README.md)

