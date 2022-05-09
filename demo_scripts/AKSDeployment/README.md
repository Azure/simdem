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

For the following variables, unless you manually added them in the env.json you will be asked to provide an input

The custom domain must be unique and fit the pattern: ^[a-z][a-z0-9-]{1,61}[a-z0-9]$
For example mycooldomain 

Do not add any capitalization or .com
```
echo $CUSTOM_DOMAIN_NAME
```

For the email address any enter a valid email. I.e sarajane@gmail.com
```
echo $SSL_EMAIL_ADDRESS
```

## Create A Resource Group
The first step is to create a resource group. You can do this with the following command

'az group create --name $RESOURCE_GROUP_NAME --location $RESOURCE_LOCATION'

```
az group create --name $RESOURCE_GROUP_NAME --location $RESOURCE_LOCATION
```

## Create an AKS Cluster 
The next step is to create an AKS Cluster. This can be done with the following command - 

az aks create --resource-group $RESOURCE_GROUP_NAME --name $AKS_CLUSTER_NAME --node-count 1 --enable-addons monitoring --generate-ssh-keys

This will take a few minutes
```
az aks create --resource-group $RESOURCE_GROUP_NAME --name $AKS_CLUSTER_NAME --node-count 1 --enable-addons monitoring --generate-ssh-keys
```

## Install az aks CLI
To manage a Kubernetes cluster, use the Kubernetes command-line client, kubectl. kubectl is already installed if you use Azure Cloud Shell.

Install kubectl locally using the az aks install-cli command:

az aks install-cli

```
az aks install-cli
```
## Download AKS Credentials
Configure kubectl to connect to your Kubernetes cluster using the az aks get-credentials command. The following command:

Downloads credentials and configures the Kubernetes CLI to use them.
Uses ~/.kube/config, the default location for the Kubernetes configuration file. Specify a different location for your Kubernetes configuration file using --file argument. WARNING - This will overwrite any existing credentials with the same entry

az aks get-credentials --resource-group $RESOURCE_GROUP_NAME --name $AKS_CLUSTER_NAME --pverwrite-existing

```
az aks get-credentials --resource-group $RESOURCE_GROUP_NAME --name $AKS_CLUSTER_NAME --overwrite-existing
```

Verify Connection
Verify the connection to your cluster using the kubectl get command. This command returns a list of the cluster nodes.

'kubectl get nodes'

```
kubectl get nodes
```

## Deploy the Application 
A test voting app is already prepared. To deploy this app run the following command 

kubectl apply -f azure-vote-start.yml

```
kubectl apply -f azure-vote-start.yml
```


Store the public IP Address as an environment variable with the following command:
'for run in {1..3}; do export IP_ADDRESS=$(kubectl get service azure-vote-front --output jsonpath='{.status.loadBalancer.ingress[0].ip}'); sleep 5; done'

```
for run in {1..3}; do export IP_ADDRESS=$(kubectl get service azure-vote-front --output jsonpath='{.status.loadBalancer.ingress[0].ip}'); sleep 5; done
```

Validate IP Address by running:
'echo $IP_ADDRESS'
After running this command you should be able to see your application running!
If the variable is empty then the command ran before the IP Address became available. Press b and run the above command manually. 
```
echo $IP_ADDRESS
```

## Deploy a new Application Gateway 
The next step is to add Application Gateway as an Ingress controller.

Create a Public IP for Application Gateway by running the following:
'az network public-ip create --name $PUBLIC_IP_NAME --resource-group $RESOURCE_GROUP_NAME --allocation-method Static --sku Standard'

```
az network public-ip create --name $PUBLIC_IP_NAME --resource-group $RESOURCE_GROUP_NAME --allocation-method Static --sku Standard
```

Create Vnet for Application Gateway by running the following:
'az network vnet create --name $VNET_NAME --resource-group $RESOURCE_GROUP_NAME --address-prefix 11.0.0.0/8 --subnet-name $SUBNET_NAME --subnet-prefix 11.1.0.0/16'
```
az network vnet create --name $VNET_NAME --resource-group $RESOURCE_GROUP_NAME --address-prefix 11.0.0.0/8 --subnet-name $SUBNET_NAME --subnet-prefix 11.1.0.0/16 
```

Create Application Gateway by running the following:
'az network application-gateway create --name $APPLICATION_GATEWAY_NAME --location $RESOURCE_LOCATION --resource-group $RESOURCE_GROUP_NAME --sku Standard_v2 --public-ip-address $PUBLIC_IP_NAME --vnet-name $VNET_NAME --subnet $SUBNET_NAME' 

This will take ~5 minutes 

```
az network application-gateway create --name $APPLICATION_GATEWAY_NAME --location $RESOURCE_LOCATION --resource-group $RESOURCE_GROUP_NAME --sku Standard_v2 --public-ip-address $PUBLIC_IP_NAME --vnet-name $VNET_NAME --subnet $SUBNET_NAME
```

## Enable the AGIC add-on in existing AKS cluster and peer Vnets through Azure CLI

Store Application Gateway ID by running the following:
'APPLICATION_GATEWAY_ID=$(az network application-gateway show --name $APPLICATION_GATEWAY_NAME --resource-group $RESOURCE_GROUP_NAME --output tsv --query "id") '

```
APPLICATION_GATEWAY_ID=$(az network application-gateway show --name $APPLICATION_GATEWAY_NAME --resource-group $RESOURCE_GROUP_NAME --output tsv --query "id") 
```

Enable Application Gateway Ingress Addon by running the following:
'az aks enable-addons --name $AKS_CLUSTER_NAME --resource-group $RESOURCE_GROUP_NAME --addon ingress-appgw --appgw-id $APPLICATION_GATEWAY_ID'

This may take a few minutes
```
az aks enable-addons --name $AKS_CLUSTER_NAME --resource-group $RESOURCE_GROUP_NAME --addon ingress-appgw --appgw-id $APPLICATION_GATEWAY_ID
```

Peer the two virtual networks together

Since we deployed the AKS cluster in its own virtual network and the Application Gateway in another virtual network, you'll need to peer the two virtual networks together in order for traffic to flow from the Application Gateway to the pods in the cluster. Peering the two virtual networks requires running the Azure CLI command two separate times, to ensure that the connection is bi-directional. The first command will create a peering connection from the Application Gateway virtual network to the AKS virtual network; the second command will create a peering connection in the other direction.

Store the node resource group by running the following:
'NODE_RESOURCE_GROUP=$(az aks show -n myAKSCluster -g $RESOURCE_GROUP_NAME -o tsv --query "nodeResourceGroup")'
```
NODE_RESOURCE_GROUP=$(az aks show -n myAKSCluster -g $RESOURCE_GROUP_NAME -o tsv --query "nodeResourceGroup")
```
Get the Vnet name by running the following:
'AKS_VNET_NAME=$(az network vnet list -g $NODE_RESOURCE_GROUP -o tsv --query "[0].name")'
```
AKS_VNET_NAME=$(az network vnet list -g $NODE_RESOURCE_GROUP -o tsv --query "[0].name")
```

Grab the Vnet ID by running the following:
'AKS_VNET_ID=$(az network vnet show -n $AKS_VNET_NAME -g $NODE_RESOURCE_GROUP -o tsv --query "id")'
```
AKS_VNET_ID=$(az network vnet show -n $AKS_VNET_NAME -g $NODE_RESOURCE_GROUP -o tsv --query "id")
```
Create the peering from Application Gateway to AKS by runnig the following:
'az network vnet peering create --name AppGWtoAKSVnetPeering -g $RESOURCE_GROUP_NAME --vnet-name'
```
az network vnet peering create --name AppGWtoAKSVnetPeering -g $RESOURCE_GROUP_NAME --vnet-name $VNET_NAME --remote-vnet $AKS_VNET_ID --allow-vnet-access 
```

Grab Id of Application Gateway Vnet:
'APPLICATION_GATEWAY_VNET_ID=$(az network vnet show -n $VNET_NAME -g $RESOURCE_GROUP_NAME -o tsv --query "id")'
```
APPLICATION_GATEWAY_VNET_ID=$(az network vnet show -n $VNET_NAME -g $RESOURCE_GROUP_NAME -o tsv --query "id")
```
Create Vnet Peering from AKS to Application Gateway
'az network vnet peering create -n AKStoAppGWVnetPeering -g $NODE_RESOURCE_GROUP --vnet-name $AKS_VNET_NAME --remote-vnet $APPLICATION_GATEWAY_VNET_ID --allow-vnet-access'
```
az network vnet peering create -n AKStoAppGWVnetPeering -g $NODE_RESOURCE_GROUP --vnet-name $AKS_VNET_NAME --remote-vnet $APPLICATION_GATEWAY_VNET_ID --allow-vnet-access
```

## Update YAML file to use AppGw Ingress by running:
'kubectl apply -f azure-vote-agic.yml'
```
kubectl apply -f azure-vote-agic.yml
```

Check that the original IP Address no longer works
```
echo $IP_ADDRESS
```

Get Ingress and Check New Address by running:
'for run in {1..3}; do kubectl get ingress; sleep 5; done'

Note - We are running this multiple times as the new IP may take a few seconds to propogate
```
for run in {1..3}; do kubectl get ingress; sleep 5; done
```
Store New IP Address by running the following command: 
'export IP_ADDRESS=$(az network public-ip show --resource-group $RESOURCE_GROUP_NAME --name $PUBLIC_IP_NAME --query ipAddress --output tsv)'

```
export IP_ADDRESS=$(az network public-ip show --resource-group $RESOURCE_GROUP_NAME --name $PUBLIC_IP_NAME --query ipAddress --output tsv)
```

Get Public IP ID

```
export PUBLIC_IP_ID=$(az network public-ip list --query "[?ipAddress!=null]|[?contains(ipAddress, '$IP_ADDRESS')].[id]" --output tsv)
```

Set Custom DNS Name by running the following:
'az network public-ip update --ids $PUBLIC_IP_ID --dns-name $CUSTOM_DOMAIN_NAME'

```
az network public-ip update --ids $PUBLIC_IP_ID --dns-name $CUSTOM_DOMAIN_NAME
```

Check custom domain to see application running - 
'az network public-ip show --ids $PUBLIC_IP_ID --query "[dnsSettings.fqdn]" --output tsv'
```
az network public-ip show --ids $PUBLIC_IP_ID --query "[dnsSettings.fqdn]" --output tsv
```

Store Custom Domain by running the following:
'export FQDN=$(az network public-ip show --ids $PUBLIC_IP_ID --query "[dnsSettings.fqdn]" --output tsv)'
```
export FQDN=$(az network public-ip show --ids $PUBLIC_IP_ID --query "[dnsSettings.fqdn]" --output tsv)
```

# Part 3 Install SSL
Create namespace for cert manager by running the following:
'kubectl create namespace cert-manager'
```
kubectl create namespace cert-manager
```

Apply Cert-Manager by running the following:

'kubectl apply -f https://github.com/jetstack/cert-manager/releases/download/v1.7.0/cert-manager.crds.yaml'

```
kubectl apply -f https://github.com/jetstack/cert-manager/releases/download/v1.7.0/cert-manager.crds.yaml
```

Label Namespace by running the following:

'kubectl label namespace cert-manager certmanager.k8s.io/disable-validation=true'
```
kubectl label namespace cert-manager certmanager.k8s.io/disable-validation=true
```

Add helm to Jetstack Repo by running the following:
'helm repo add jetstack https://charts.jetstack.io'
```
helm repo add jetstack https://charts.jetstack.io
```
Update Repo by running the following:
'helm repo update'
```
helm repo update
```

Install Cert-Manager via helm by running the following:
'helm install cert-manager jetstack/cert-manager --namespace cert-manager --version v1.7.0'
```
helm install cert-manager jetstack/cert-manager --namespace cert-manager --version v1.7.0
```

Apply CertIssuer YAML File by running the following:
'envsubst < cluster-issuer-prod.yaml | kubectl apply -f -'
```
envsubst < cluster-issuer-prod.yaml | kubectl apply -f -
```

Apply Updated YAML file with SSL Certby running the following:
envsubst < azure-vote-agic-ssl.yml | kubectl apply -f -
```
envsubst < azure-vote-agic-ssl.yml | kubectl apply -f -
```

Check to make sure Ingress is working by running:
'for run in {1..3}; do kubectl get ingress; sleep 5; done'

Note - We are running this multiple times to show the Lets Encrypt Service validating domain ownership
```
for run in {1..3}; do kubectl get ingress; sleep 5; done
```

Check SSL Certificate by running the following command:
'kubectl get certificate'
```
kubectl get certificate
```

## Browse your secured AKS Deployment!
Paste the following link into your browser with https as the prefix
```
az network public-ip show --ids $PUBLIC_IP_ID --query "[dnsSettings.fqdn]" --output tsv
```

