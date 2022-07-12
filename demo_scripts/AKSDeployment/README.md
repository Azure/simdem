# Tutorial: Deploy a Scalable & Secure Azure Kubernetes Service cluster using the Azure CLI
Azure Kubernetes Service provides a powerful way to manage Kubernetes applications which are Portable, extensibile, and when combined with Azure infrastructure highly scalable. This tutorial covers the steps you in creating an Azure Kubernetes Web Application with a custom domain that is secured via https.

## Prerequisites
 - Access to Azure CLI with an active subscription. To install Azure CLI see https://docs.microsoft.com/en-us/cli/azure/install-azure-cli.
 - If you have multiple Azure subscriptions, select the appropriate subscription ID in which the resources should be billed using the az account command.
 - This tutorial requires version 2.0.64 or later of the Azure CLI. If using Azure Cloud Shell, the latest version is already installed.

 - If you're using a local installation, sign in to the Azure CLI by using the az login command. To finish the authentication process, follow the steps displayed in your terminal. For other sign-in options, see Sign in with the Azure CLI..
 - Helm installed and configured. To install Helm see  https://helm.sh/docs/intro/install/.
- Consider using the Bash enviornment in Azure Cloud Shell
- Envsubst installed. This can be installed in Cloud Shell by running pip install envsubst

## Setup

### Define Default Command Line Variables 
This tutorial will use command line variables. Copy and run the following  the following to set default command line variables 

```
export RESOURCE_GROUP_NAME="myResourceGroup"
export RESOURCE_LOCATION="eastus"
export AKS_CLUSTER_NAME "myAKSCluster"
export PUBLIC_IP_NAME="myPublicIp"
export VNET_NAME="myVnet"
export SUBNET_NAME="mySubnet"
export APPLICATION_GATEWAY_NAME="myApplicationGateway"
export APPGW_TO_AKS_PEERING_NAME="AppGWtoAKSVnetPeering"
export AKS_TO_APPGW_PEERING_NAME="AKStoAppGWVnetPeering"
```

### Define Custom Command Line Variables 
Custom values are required for the following inputs.

We will now choose and define the custom domain which your application will use. The application will be reachable at {mycustomdomain}.eastus.cloudapp.azure.com
 
 Run the following command with a unique custom domain:
>[!Note] Do not add any capitalization or .com. The custom domain must be unique and fit the pattern: ^[a-z][a-z0-9-]{1,61}[a-z0-9]$


```
echo $CUSTOM_DOMAIN_NAME
```

You can validate the custom domain works by running the following 
```
if [[ ! $CUSTOM_DOMAIN_NAME =~ ^[a-z][a-z0-9-]{1,61}[a-z0-9] ]]; then echo "Invalid Domain, run'export CUSTOM_DOMAIN_NAME="customdomainname"' again and choose a new domain"; else echo "Custom Domain Set!"; fi; 
```

Set a valid email address for SSL validation by running the following:
```
echo $SSL_EMAIL_ADDRESS
```

## Create A Resource Group
An Azure resource group is a logical group in which Azure resources are deployed and managed. When you create a resource group, you are prompted to specify a location. This location is:
  - The storage location of your resource group metadata.
  - Where your resources will run in Azure if you don't specify another region during resource creation.

Validate Resource Group does not already exist. If it does, select a new resource group name by running the following:

```
if [ "$(az group exists --name $RESOURCE_GROUP_NAME)" = 'true' ]; then export RAND=$RANDOM; export RESOURCE_GROUP_NAME="$RESOURCE_GROUP_NAME$RAND"; echo "Your new Resource Group Name is $RESOURCE_GROUP_NAME"; fi
```

Create a resource group using the az group create command:
```
az group create --name $RESOURCE_GROUP_NAME --location $RESOURCE_LOCATION
```
The following is output for successful resource group creation

Results:

```expected_similarity=0.5
{
  "id": "/subscriptions/bb318642-28fd-482d-8d07-79182df07999/resourceGroups/testResourceGroup24763",
  "location": "eastus",
  "managedBy": null,
  "name": "testResourceGroup",
  "properties": {
    "provisioningState": "Succeeded"
  },
  "tags": null,
  "type": "Microsoft.Resources/resourceGroups"
}
```

## Create AKS Cluster 
Create an AKS cluster using the az aks create command with the --enable-addons monitoring parameter to enable Container insights. The following example creates a cluster named myAKSCluster with one node:

```
az aks create --resource-group $RESOURCE_GROUP_NAME --name $AKS_CLUSTER_NAME --node-count 1 --enable-addons monitoring --generate-ssh-keys
```

## Connect to the cluster
To manage a Kubernetes cluster, use the Kubernetes command-line client, kubectl. kubectl is already installed if you use Azure Cloud Shell.

1. Install az aks CLI locally using the az aks install-cli command

```
if ! [ -x "$(command -v kubectl)" ]; then az aks install-cli; fi
```

2. Configure kubectl to connect to your Kubernetes cluster using the az aks get-credentials command. The following command:
    - Downloads credentials and configures the Kubernetes CLI to use them.
    - Uses ~/.kube/config, the default location for the Kubernetes configuration file. Specify a different location for your Kubernetes configuration file using --file argument. 

> [!WARNING]
> This will overwrite any existing credentials with the same entry

```
az aks get-credentials --resource-group $RESOURCE_GROUP_NAME --name $AKS_CLUSTER_NAME --overwrite-existing
```

3. Verify the connection to your cluster using the kubectl get command. This command returns a list of the cluster nodes.

```
kubectl get nodes
```

## Deploy the Application 

A [Kubernetes manifest file](https://docs.microsoft.com/en-us/azure/aks/concepts-clusters-workloads#deployments-and-yaml-manifests) defines a cluster's desired state, such as which container images to run.

In this quickstart, you will use a manifest to create all objects needed to run the [Azure Vote application](https://github.com/Azure-Samples/azure-voting-app-redis). This manifest includes two Kubernetes deployments:

- The sample Azure Vote Python applications.
- A Redis instance.

Two [Kubernetes Services](https://docs.microsoft.com/en-us/azure/aks/concepts-network#services) are also created:

- An internal service for the Redis instance.
- An external service to access the Azure Vote application from the internet.

1. Create a file named azure-vote.yaml and copy in the following manifest - 
https://github.com/Azure/simdem/blob/jamesserDev/demo_scripts/AKSDeployment/azure-vote-start.yml

    - If you use the Azure Cloud Shell, this file can be created using code, vi, or nano as if working on a virtual or physical system.


2. Deploy the application using the [kubectl apply](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#apply) command and specify the name of your YAML manifest:
```
kubectl apply -f azure-vote-start.yml
```

## Test the Application
When the application runs, a Kubernetes service exposes the application front end to the internet. This process can take a few minutes to complete.

Check progress using the kubectl get service command.

```
kubectl get service
```

Store the public IP Address as an environment variable for later use.
>[!Note]
> This commmand loops for 2 minutes and queries the output of kubectl get service for the IP Address. Sometimes it can take a few seconds to propogate correctly 
```
runtime="2 minute"; endtime=$(date -ud "$runtime" +%s); while [[ $(date -u +%s) -le $endtime ]]; do export IP_ADDRESS=$(kubectl get service azure-vote-front --output jsonpath='{.status.loadBalancer.ingress[0].ip}'); if ! [ -z $IP_ADDRESS ]; then break; else sleep 10; fi; done
```

Run the following command to obtain the IP Address
```
echo $IP_ADDRESS
```

To see the Azure Vote app in action, open a web browser to the external IP address of the application.

# Part 2: Scale your Application

## Add Application Gateway Ingress Controller
The Application Gateway Ingress Controller (AGIC) is a Kubernetes application, which makes it possible for Azure Kubernetes Service (AKS) customers to leverage Azure's native Application Gateway L7 load-balancer to expose cloud software to the Internet. AGIC monitors the Kubernetes cluster it is hosted on and continuously updates an Application Gateway, so that selected services are exposed to the Internet

AGIC helps eliminate the need to have another load balancer/public IP in front of the AKS cluster and avoids multiple hops in your datapath before requests reach the AKS cluster. Application Gateway talks to pods using their private IP directly and does not require NodePort or KubeProxy services. This also brings better performance to your deployments.

## Deploy a new Application Gateway 
1. Create a Public IP for Application Gateway by running the following:
```
az network public-ip create --name $PUBLIC_IP_NAME --resource-group $RESOURCE_GROUP_NAME --allocation-method Static --sku Standard
```

2. Create a Virtual Network(Vnet) for Application Gateway by running the following:
```
az network vnet create --name $VNET_NAME --resource-group $RESOURCE_GROUP_NAME --address-prefix 11.0.0.0/8 --subnet-name $SUBNET_NAME --subnet-prefix 11.1.0.0/16 
```

3. Create Application Gateway by running the following:

> [!NOTE] 
> This will take around 5 minutes 
```
az network application-gateway create --name $APPLICATION_GATEWAY_NAME --location $RESOURCE_LOCATION --resource-group $RESOURCE_GROUP_NAME --sku Standard_v2 --public-ip-address $PUBLIC_IP_NAME --vnet-name $VNET_NAME --subnet $SUBNET_NAME
```

## Enable the AGIC add-on in existing AKS cluster 

1. Store Application Gateway ID by running the following:
```
APPLICATION_GATEWAY_ID=$(az network application-gateway show --name $APPLICATION_GATEWAY_NAME --resource-group $RESOURCE_GROUP_NAME --output tsv --query "id") 
```

2. Enable Application Gateway Ingress Addon by running the following:

> [!NOTE]
> This will take a few minutes
```
az aks enable-addons --name $AKS_CLUSTER_NAME --resource-group $RESOURCE_GROUP_NAME --addon ingress-appgw --appgw-id $APPLICATION_GATEWAY_ID
```

3. Store the node resource as an environment variable group by running the following:
```
NODE_RESOURCE_GROUP=$(az aks show --name myAKSCluster --resource-group $RESOURCE_GROUP_NAME --output tsv --query "nodeResourceGroup")
```
4. Store the Vnet name as an environment variable by running the following:
```
AKS_VNET_NAME=$(az network vnet list --resource-group $NODE_RESOURCE_GROUP --output tsv --query "[0].name")
```

5. Store the Vnet ID as an environment variable by running the following:
```
AKS_VNET_ID=$(az network vnet show --name $AKS_VNET_NAME --resource-group $NODE_RESOURCE_GROUP --output tsv --query "id")
```
## Peer the two virtual networks together 
Since we deployed the AKS cluster in its own virtual network and the Application Gateway in another virtual network, you'll need to peer the two virtual networks together in order for traffic to flow from the Application Gateway to the pods in the cluster. Peering the two virtual networks requires running the Azure CLI command two separate times, to ensure that the connection is bi-directional. The first command will create a peering connection from the Application Gateway virtual network to the AKS virtual network; the second command will create a peering connection in the other direction.

1. Create the peering from Application Gateway to AKS by runnig the following:
```
az network vnet peering create --name $APPGW_TO_AKS_PEERING_NAME --resource-group $RESOURCE_GROUP_NAME --vnet-name $VNET_NAME --remote-vnet $AKS_VNET_ID --allow-vnet-access 
```

2. Store Id of Application Gateway Vnet As enviornment variable by running the following:
```
APPLICATION_GATEWAY_VNET_ID=$(az network vnet show --name $VNET_NAME --resource-group $RESOURCE_GROUP_NAME --output tsv --query "id")
```
3. Create Vnet Peering from AKS to Application Gateway
```
az network vnet peering create --name $AKS_TO_APPGW_PEERING_NAME --resource-group $NODE_RESOURCE_GROUP --vnet-name $AKS_VNET_NAME --remote-vnet $APPLICATION_GATEWAY_VNET_ID --allow-vnet-access
```
4. Store New IP address as environment variable by running the following command:
```
runtime="2 minute"; endtime=$(date -ud "$runtime" +%s); while [[ $(date -u +%s) -le $endtime ]]; do export IP_ADDRESS=$(az network public-ip show --resource-group $RESOURCE_GROUP_NAME --name $PUBLIC_IP_NAME --query ipAddress --output tsv); if ! [ -z $IP_ADDRESS ]; then break; else sleep 10; fi; done
```

## Apply updated application YAML complete with AGIC

1. Create a file named azure-vote-agic-yaml and copy in the following manifest - https://github.com/Azure/simdem/blob/jamesserDev/demo_scripts/AKSDeployment/azure-vote-agic.yml

    - If you use the Azure Cloud Shell, this file can be created using code, vi, or nano as if working on a virtual or physical system.


2. Deploy the updated Voting App AGIC YAML file with Application Gateway Ingress added by running the following command:

```
kubectl apply -f azure-vote-agic.yml
```

## Check that the application is reachable
Now that the Application Gateway is set up to serve traffic to the AKS cluster, let's verify that your application is reachable. 

Check that the sample application you created is up and running by either visiting the IP address of the Application Gateway that get from running the following command or check with curl. It may take Application Gateway a minute to get the update, so if the Application Gateway is still in an "Updating" state on Portal, then let it finish before trying to reach the IP address. Run the following to check the status:
```
kubectl get ingress
```

Run the following command to obtain the IP Address of Application Gateway
```
echo $IP_ADDRESS
```

To see the Azure Vote app in action, open a web browser to the external IP address of the application.


# Part 3: Custom Domain and HTTPS
## Add custom domain to AGIC
Now that Application Gateway Ingress has been added, the next step is to add a custom domain. This will allow the endpoint to be reached by a human readable URL as well as allow for SSL Termination at the endpoint.

1. Store Unique ID of the Public IP Address as an environment variable by running the following:
```
export PUBLIC_IP_ID=$(az network public-ip list --query "[?ipAddress!=null]|[?contains(ipAddress, '$IP_ADDRESS')].[id]" --output tsv)
```

2. Update public IP to respond to custom domain requests by running the following:
```
az network public-ip update --ids $PUBLIC_IP_ID --dns-name $CUSTOM_DOMAIN_NAME
```

3. Run the following command to see the fully qualified domain name (FQDN) of your application. 
```
az network public-ip show --ids $PUBLIC_IP_ID --query "[dnsSettings.fqdn]" --output tsv
```
     Validate the domain works by opening a web browser to the FQDN of the application.

4. Store the custom domain as en enviornment variable. This will be used later when setting up https termination.
```
export FQDN=$(az network public-ip show --ids $PUBLIC_IP_ID --query "[dnsSettings.fqdn]" --output tsv)
```

## Add HTTPS termination to custom domain 
At this point in the tutorial you have an AKS web app with Application Gateway as the Ingress controller and a custom domain you can use to access your application. The next step is to add an SSL certificate to the domain so that users can reach your application securely via https.  

### Set Up Cert Manager
In order to add HTTPS we are going to use Cert Manager. Cert Manager is an open source tool used to obtain and manage SSL certificate for Kubernetes deployments. Cert Manager will obtain certificates from a variety of Issuers, both popular public Issuers as well as private Issuers, and ensure the certificates are valid and up-to-date, and will attempt to renew certificates at a configured time before expiry.

1. In order to install cert-manager, we must first create a namespace to run it in. This tutorial will install cert-manager into the cert-manager namespace. It is possible to run cert-manager in a different namespace, although you will need to make modifications to the deployment manifests.
```
kubectl create namespace cert-manager
```

2. We can now install cert-manager. All resources are included in a single YAML manifest file. This can be installed by running the following:
```
kubectl apply -f https://github.com/jetstack/cert-manager/releases/download/v1.7.0/cert-manager.crds.yaml
```


3. Add the certmanager.k8s.io/disable-validation: "true" label to the cert-manager namespace by running the following. This will allow the system resources that cert-manager requires to bootstrap TLS to be created in its own namespace.
```
kubectl label namespace cert-manager certmanager.k8s.io/disable-validation=true
```

### Obtain certificate via Helm Charts
Helm is a Kubernetes deployment tool for automating creation, packaging, configuration, and deployment of applications and services to Kubernetes clusters.

Cert-manager provides Helm charts as a first-class method of installation on Kubernetes.

1. Add the Jetstack Helm repository
This repository is the only supported source of cert-manager charts. There are some other mirrors and copies across the internet, but those are entirely unofficial and could present a security risk.
```
helm repo add jetstack https://charts.jetstack.io
```

2. Update local Helm Chart repository cache 
```
helm repo update
```

3. Install Cert-Manager addon via helm by running the following:
```
helm install cert-manager jetstack/cert-manager --namespace cert-manager --version v1.7.0
```

4. Deploy Cluster Issuer 

    ClusterIssuers are Kubernetes resources that represent certificate authorities (CAs) that are able to generate signed certificates by honoring certificate signing requests. All cert-manager certificates require a referenced issuer that is in a ready condition to attempt to honor the request.

    - Create a file named cluster-issuer-prod.yaml and copy in the following manifest - https://github.com/Azure/simdem/blob/jamesserDev/demo_scripts/AKSDeployment/cluster-issuer-prod.yaml

    - If you use the Azure Cloud Shell, this file can be created using code, vi, or nano as if working on a virtual or physical system.

- Deploy the Cluster Issuer YAML file by running the following command:
  >[!NOTE] envsubst will replace variables in the YAML file with command line variables previosuly defined
```
envsubst < cluster-issuer-prod.yaml | kubectl apply -f -
```

5. Create and deploy Updated YAML manifest which includes ssl termination
 - Create a file named azure-vote-agic-ssl.yml and copy in the following manifest -https://github.com/Azure/simdem/blob/jamesserDev/demo_scripts/AKSDeployment/azure-vote-agic-ssl.yml


- Deploy the YAML file complete with SSL termination by running the following command: 
    >[!NOTE] envsubst will replace variables in the YAML file with command line variables previosuly defined

```
envsubst < azure-vote-agic-ssl.yml | kubectl apply -f -
```
## Validate application is working

Wait for SSL certificate to issue. The following command will query the status of the SSL certificate for 3 minutes.
 In rare occasions it may take up to 15 minutes for Lets Encrypt to issue a successful challenge and the ready state to be 'True'
```
runtime="10 minute"; endtime=$(date -ud "$runtime" +%s); while [[ $(date -u +%s) -le $endtime ]]; do STATUS=$(kubectl get certificate --output jsonpath={..status.conditions[0].status}); echo $STATUS; if [ "$STATUS" = 'True' ]; then break; else sleep 10; fi; done
```

Validate SSL certificate is True by running the follow command:
```
kubectl get certificate --output jsonpath={..status.conditions[0].status}
```

The following is a successful output

Results:
```expected_similarity=0.8
True
```

## Browse your AKS Deployment Secured via HTTPS!
Run the following command to get the HTTPS endpoint for your application:

>[!Note]
> It often takes 2-3 minutes for the SSL certificate to propogate and the site to be reachable via https 
```
echo https://$FQDN
```
To see the Azure Vote app in action, open a web browser to the HTTPS Endpoint of the Application.