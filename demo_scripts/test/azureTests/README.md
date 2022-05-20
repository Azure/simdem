
# AKS Script Test

Welcome to this tutorial where we will take you step by step in creating an AKS Application with a custom domain that is secured via https. This tutorial assumes you are logged into Azure CLI already and have selected a subscription to use with the CLI. It also assumes that you have helm installed (Instructions ca be found here https://helm.sh/docs/intro/install/). If you have not done this already. Press b and hit ctl c to exit the program.

To Login to Az CLI and select a subscription 
'az login' followed by 'az account list --output table' and 'az account set --subscription "name of subscription to use"'

To Install Az CLI
If you need to install Azure CLI run the following command - curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash


Assuming the pre requisites are met press enter to proceed

## Define Command Line Variables 
Most of these variables should be set to a smart default. However, if you want to change them
press b and run the command export VARIABLE_NAME="new variable value"

```
echo $RESOURCE_GROUP_NAME
echo $RESOURCE_LOCATION
echo $AKS_CLUSTER_NAME
echo $PUBLIC_IP_NAME
echo $VNET_NAME
echo $SUBNET_NAME
echo $APPLICATION_GATEWAY_NAME
```

For the following variables, unless you manually added them in the env.json, you will be asked to provide an input

The custom domain must be unique and fit the pattern: ^[a-z][a-z0-9-]{1,61}[a-z0-9]$
For example mycooldomain - this domain is already taken btw :) 

Note - Do not add any capitalization or .com
```
if [[ ! $CUSTOM_DOMAIN_NAME =~ ^[a-z][a-z0-9-]{1,61}[a-z0-9] ]]; then echo "Invalid Domain, re enter your domain by pressing b and running 'export CUSTOM_DOMAIN_NAME="customdomainname"' then press r to re-run the previous command and validate the custom domain"; else echo "Custom Domain Set!"; fi; 
```

For the email address any enter a valid email. I.e sarajane@gmail.com
```
echo $SSL_EMAIL_ADDRESS
```

## Create A Resource Group
The first step is to create a resource group.

Validate that ResourceGroup does not already exist 

```
if [ "$(az group exists --name $RESOURCE_GROUP_NAME)" = 'true' ]; then export RAND=$RANDOM; export RESOURCE_GROUP_NAME="$RESOURCE_GROUP_NAME$RAND"; echo "Your new Resource Group Name is $RESOURCE_GROUP_NAME"; fi
```

Create Resource Group
```
az group create --name $RESOURCE_GROUP_NAME --location $RESOURCE_LOCATION
```

## Create an AKS Cluster 
The next step is to create an AKS Cluster. This can be done with the following command - 

This will take a few minutes
```
az aks create --resource-group $RESOURCE_GROUP_NAME --name $AKS_CLUSTER_NAME --node-count 1 --enable-addons monitoring --generate-ssh-keys
```

## Install az aks CLI locally using the az aks install-cli command
To manage a Kubernetes cluster, use the Kubernetes command-line client, kubectl. kubectl is already installed if you use Azure Cloud Shell.

```
if ! [ -x "$(command -v kubectl)" ]; then az aks install-cli; fi
```
## Download AKS Credentials
Configure kubectl to connect to your Kubernetes cluster using the az aks get-credentials command. The following command:

Downloads credentials and configures the Kubernetes CLI to use them.
Uses ~/.kube/config, the default location for the Kubernetes configuration file. Specify a different location for your Kubernetes configuration file using --file argument. WARNING - This will overwrite any existing credentials with the same entry

```
az aks get-credentials --resource-group $RESOURCE_GROUP_NAME --name $AKS_CLUSTER_NAME --overwrite-existing
```

Verify Connection
Verify the connection to your cluster using the kubectl get command. This command returns a list of the cluster nodes.

```
kubectl get nodes
```

## Deploy the Application 
A test voting app is already prepared. To deploy this app run the following command 
```
kubectl apply -f azure-vote-start.yml
```

Store the public IP Address as an environment variable:
```
runtime="2 minute"; endtime=$(date -ud "$runtime" +%s); while [[ $(date -u +%s) -le $endtime ]]; do export IP_ADDRESS=$(kubectl get service azure-vote-front --output jsonpath='{.status.loadBalancer.ingress[0].ip}'); if ! [ -z $IP_ADDRESS ]; then break; else sleep 10; fi; done
```

Validate IP Address by running:
After running this command you should be able to see your application running! 
Note - The IP may take ~30 seconds to resolve
```
echo $IP_ADDRESS
```

## Deploy a new Application Gateway 
The next step is to add Application Gateway as an Ingress controller.

Create a Public IP for Application Gateway by running the following:
```
az network public-ip create --name $PUBLIC_IP_NAME --resource-group $RESOURCE_GROUP_NAME --allocation-method Static --sku Standard
```

Create Vnet for Application Gateway by running the following:
```
az network vnet create --name $VNET_NAME --resource-group $RESOURCE_GROUP_NAME --address-prefix 11.0.0.0/8 --subnet-name $SUBNET_NAME --subnet-prefix 11.1.0.0/16 
```

Create Application Gateway by running the following:

This will take ~5 minutes 
```
az network application-gateway create --name $APPLICATION_GATEWAY_NAME --location $RESOURCE_LOCATION --resource-group $RESOURCE_GROUP_NAME --sku Standard_v2 --public-ip-address $PUBLIC_IP_NAME --vnet-name $VNET_NAME --subnet $SUBNET_NAME
```

## Enable the AGIC add-on in existing AKS cluster and peer Vnets through Azure CLI

Store Application Gateway ID by running the following:
```
APPLICATION_GATEWAY_ID=$(az network application-gateway show --name $APPLICATION_GATEWAY_NAME --resource-group $RESOURCE_GROUP_NAME --output tsv --query "id") 
```

Enable Application Gateway Ingress Addon by running the following:

This may take a few minutes
```
az aks enable-addons --name $AKS_CLUSTER_NAME --resource-group $RESOURCE_GROUP_NAME --addon ingress-appgw --appgw-id $APPLICATION_GATEWAY_ID
```

Peer the two virtual networks together

Since we deployed the AKS cluster in its own virtual network and the Application Gateway in another virtual network, you'll need to peer the two virtual networks together in order for traffic to flow from the Application Gateway to the pods in the cluster. Peering the two virtual networks requires running the Azure CLI command two separate times, to ensure that the connection is bi-directional. The first command will create a peering connection from the Application Gateway virtual network to the AKS virtual network; the second command will create a peering connection in the other direction.

Store the node resource group by running the following:
```
NODE_RESOURCE_GROUP=$(az aks show --name myAKSCluster --resource-group $RESOURCE_GROUP_NAME --output tsv --query "nodeResourceGroup")
```
Store the Vnet name by running the following:
```
AKS_VNET_NAME=$(az network vnet list --resource-group $NODE_RESOURCE_GROUP --output tsv --query "[0].name")
```

Store the Vnet ID by running the following:
```
AKS_VNET_ID=$(az network vnet show --name $AKS_VNET_NAME --resource-group $NODE_RESOURCE_GROUP --output tsv --query "id")
```
Create the peering from Application Gateway to AKS by runnig the following:
```
az network vnet peering create --name $APPGW_TO_AKS_PEERING_NAME --resource-group $RESOURCE_GROUP_NAME --vnet-name $VNET_NAME --remote-vnet $AKS_VNET_ID --allow-vnet-access 
```

Grab Id of Application Gateway Vnet:
```
APPLICATION_GATEWAY_VNET_ID=$(az network vnet show --name $VNET_NAME --resource-group $RESOURCE_GROUP_NAME --output tsv --query "id")
```
Create Vnet Peering from AKS to Application Gateway
```
az network vnet peering create --name $AKS_TO_APPGW_PEERING_NAME --resource-group $NODE_RESOURCE_GROUP --vnet-name $AKS_VNET_NAME --remote-vnet $APPLICATION_GATEWAY_VNET_ID --allow-vnet-access
```

## Update YAML file to use AppGw Ingress:
```
kubectl apply -f azure-vote-agic.yml
```

Validate that the original IP Address is no longer working
```
echo $IP_ADDRESS
```

Get Ingress and Check New Address
```
kubectl get ingress
```
Store New IP Address 

```
runtime="2 minute"; endtime=$(date -ud "$runtime" +%s); while [[ $(date -u +%s) -le $endtime ]]; do export IP_ADDRESS=$(az network public-ip show --resource-group $RESOURCE_GROUP_NAME --name $PUBLIC_IP_NAME --query ipAddress --output tsv); if ! [ -z $IP_ADDRESS ]; then break; else sleep 10; fi; done
```

Store Public IP ID
```
export PUBLIC_IP_ID=$(az network public-ip list --query "[?ipAddress!=null]|[?contains(ipAddress, '$IP_ADDRESS')].[id]" --output tsv)
```

Set Public IP to Custom DNS Name by running the following:
```
az network public-ip update --ids $PUBLIC_IP_ID --dns-name $CUSTOM_DOMAIN_NAME
```

Check custom domain to see application running - 
```
az network public-ip show --ids $PUBLIC_IP_ID --query "[dnsSettings.fqdn]" --output tsv
```

Store Custom Domain by running the following:
```
export FQDN=$(az network public-ip show --ids $PUBLIC_IP_ID --query "[dnsSettings.fqdn]" --output tsv)
```

# Part 3 Install SSL
Create namespace for cert manager by running the following:
```
kubectl create namespace cert-manager
```

Apply Cert-Manager
```
kubectl apply -f https://github.com/jetstack/cert-manager/releases/download/v1.7.0/cert-manager.crds.yaml
```

Label the Namespace
```
kubectl label namespace cert-manager certmanager.k8s.io/disable-validation=true
```

Add jetstack addon via helm
```
helm repo add jetstack https://charts.jetstack.io
```

Update Repo
```
helm repo update
```

Install Cert-Manager addon via helm by running the following:
```
helm install cert-manager jetstack/cert-manager --namespace cert-manager --version v1.7.0
```

Apply CertIssuer YAML File 
```
envsubst < cluster-issuer-prod.yaml | kubectl apply -f -
```

Apply Updated AKS Application via YAML file with SSL
```
envsubst < azure-vote-agic-ssl.yml | kubectl apply -f -
```

Check to make sure Ingress is working
```
kubectl get ingress
```

Check SSL Certificate - The following command will query the status of the SSL certificate for 3 minutes. 
In rare occasions it may take up to 15 minutes for Lets Encrypt to issue a successful challenge and the ready state to be 'True'
```
runtime="10 minute"; endtime=$(date -ud "$runtime" +%s); while [[ $(date -u +%s) -le $endtime ]]; do STATUS=$(kubectl get certificate --output jsonpath={..status.conditions[0].status}); echo $STATUS; if [ "$STATUS" = 'True' ]; then break; else sleep 10; fi; done
```

for testing purposes - If the SSL Certificate 
```
kubectl get certificate --output jsonpath={..status.conditions[0].status}
```
Results:

```expected_similarity=0.8
True
```

Validate certificate status is true - Sometimes there may be a slight delay
```
kubectl get certificate
```

## Browse your secured AKS Deployment!
Paste the following link into your browser with https:// as the prefix

```
echo https://$FQDN
```


# Clean up resources 
```
az group delete --name $RESOURCE_GROUP_NAME --no-wait --yes
```