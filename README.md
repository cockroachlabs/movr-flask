# MovR

## Overview

MovR is a fictional vehicle-sharing company. 

This repo contains the source code for the MovR application, which is comprised of the following:

- A SQLAlchemy mapping of the [MovR database](https://www.cockroachlabs.com/docs/dev/movr.html)
- A REST API to the MovR database mapping
- A web server that hosts an interactive web UI for MovR

For more information about MovR, see the [MovR webpage](https://www.cockroachlabs.com/docs/dev/movr.html).

## Debugging

### Database set-up

In production, you want to start a secure CockroachDB cluster, with nodes on machines located in different areas of the world. For debugging purposes, you can just use the [`cockroach demo`](cockroach-demo.html) command. This command starts up an insecure, virtual nine-node cluster.

1. If you haven't already, download [CockroachDB](https://www.cockroachlabs.com/docs/stable/install-cockroachdb-mac.html).

1. Run `cockroach demo`, with the `--nodes` and `--demo-locality` flags. The database schema provided in this repo assumes the GCP region names. 

    ~~~ shell
    $ cockroach demo \
    --nodes=9 \
    --demo-locality=region=gcp-us-east1:region=gcp-us-east1:region=gcp-us-east1:region=gcp-us-west1:region=gcp-us-west1:region=gcp-us-west1:region=gcp-europe-west1:region=gcp-europe-west1:region=gcp-europe-west1
    ~~~

    ~~~
    root@127.0.0.1:<some_port>/movr> 
    ~~~

    Keep this terminal window open. Closing it will shut down the virtual cluster.

1. Copy the connection string at the prompt (e.g., `root@127.0.0.1:<some_port>/movr`). 

1. In a separate terminal window, run the following command to load `dbinit.sql` to the demo database:

    ~~~ shell
    $ cockroach sql --insecure --url='postgresql://root@127.0.0.1:<some_port>/movr' < dbinit.sql
    ~~~

### Application set-up

In production, you probably want to containerize your application and deploy it with k8s. For debugging, use `pipenv`, a tool that manages dependencies with `pip` and creates virtual environments with `virtualenv`.

1. Run the following command to initialize the project's virtual environment:

    ~~~ shell
    $ pipenv --three
    ~~~

1. Run the following command to install the packages listed in the `Pipfile`:

    ~~~ shell
    $ pipenv install
    ~~~

1. Pipenv automatically sets any variables defined in a `.env` file as environment variables in a Pipenv virtual environment. To connect to a SQL database (including CockroachDB!) from a client, you need a [SQL connection string](https://en.wikipedia.org/wiki/Connection_string). 

    So, create a file named `.env`, and then define the connection string in that file as the `DB_URI` environment variable. Note that for SQLAlchemy, the connection string protocol needs to be specific to the CockroachDB dialect.

    For example:

    ~~~
    DB_URI = 'cockroachdb://root@127.0.0.1:52382/movr'
    ~~~

    You can also specify a Google Maps API key here, but you might need to create a new key and restrict that key to your local IP address.

1. Activate the virtual environment:

    ~~~ shell
    $ pipenv shell
    ~~~

    The prompt should now read `~bash-3.2$`. From this shell, you can run any Python3 application with the required dependencies that you listed in the `Pipfile` and the environment variables that you listed in the `.env` file. You can exit the shell subprocess at any time with a simple `exit` command.

1. To test out the application, you can simply run the server file:

    ~~~ shell
    $ python3 server.py
    ~~~

    You can alternatively use [gunicorn](https://gunicorn.org/) for the server.

    ~~~ shell
    $ gunicorn -b localhost:8000 server:app
    ~~~

1. Navigate to the URL provided to test out the application.

## Multi-region Deployment

### Database Deployment (Cockroach Cloud)

To deploy CockroachDB in multiple regions, we recommend that you use [Cockroach Cloud](https://cockroachlabs.cloud):

1. Create a multi-region CockroachCloud cluster, with GCP, in regions us-west1, us-east1, europe-west1.

1. After you create the CC cluster, select **Connect**, and create a user and network. In this example, we just make the connection public. See https://www.cockroachlabs.com/docs/cockroachcloud/stable/cockroachcloud-connect-to-your-cluster.html for instructions.

1. After you create the user and password, copy the connection strings for each region, with the user and password specified. 

1. Download the cluster cert to your local machine (it's the same for all regions).

1. Open a separate terminal and run the `dbinit.sql` file on the running cluster to initialize the database. You can connect to the databse from any node on the cluster.

    ~~~ shell
    $ cockroach sql --url any-connection-string < dbinit.sql
    ~~~

    **Note:** You need to specify the password in the connection string!

    e.g.,
    ~~~ shell
    $ cockroach sql --url \ 'postgresql://user:password@region.cockroachlabs.cloud:26257/defaultdb?sslmode=verify-full&sslrootcert=certs-dir/movr-app-ca.crt' < dbinit.sql
    ~~~

**Note:** You can also deploy CRDB manually. For instructions, see the [Manual Deployment](manual-deployment.html) page of the Cockroach Labs documentation site.

### Application Deployment

To deploy the application globally, we recommend that you use a major cloud provider with a global load-balancing service and a Kubernetes engine. For our deployment, we use GCP. To serve a secure web application, you also need a public domain name!

1. If you don't have a glcoud account, create one at https://cloud.google.com/.

1. Create a gcloud project on the [GCP console](https://console.cloud.google.com/).

1. Enable the [Google Maps Embed API](https://console.cloud.google.com/apis/library), create an API key, restrict the API key to all subdomains of your domain name (e.g. `https://site.com/*`), and retrieve the API key.

1. Configure/authorize the gcloud CLI to use your project and region.

    ~~~ shell
    $ gcloud init
    $ gcloud auth login
    $ gcloud auth application-default login
    ~~~

1. Install kubectl.

    ~~~ shell
    $ gcloud components install kubectl
    ~~~

1. Build and run the docker image locally.

    ~~~ shell
    $ docker build -t gcr.io/<gcp_project>/movr-app:v1 .
    ~~~

    If there are no errors, the container built successfully.

1. Push the Docker image to the project’s gcloud container registry.

    e.g.,
    ~~~ shell
    $ docker push gcr.io/<gcp_project>/movr-app:v1
    ~~~

1. Create a K8s cluster for all three regions.

    ~~~ shell
    $ gcloud config set compute/zone us-east1-b && \
      gcloud container clusters create movr-us-east
    $ gcloud config set compute/zone us-west1-b && \
      gcloud container clusters create movr-us-west
    $ gcloud config set compute/zone europe-west1-b && \
      gcloud container clusters create movr-europe-west
    ~~~

1. Add the container credentials to kubeconfig.

    ~~~ shell
    $ KUBECONFIG=~/mcikubeconfig gcloud container clusters get-credentials --zone=us-east1-b movr-us-east
    $ KUBECONFIG=~/mcikubeconfig gcloud container clusters get-credentials --zone=us-west1-b movr-us-west
    $ KUBECONFIG=~/mcikubeconfig gcloud container clusters get-credentials --zone=europe-west1-b movr-europe-west
    ~~~

1. For each cluster context, create a secret for the connection string, Google Maps API, and the certs, and then create the k8s deployment and service using the `movr.yaml` manifest file. To get the context for the cluser, run `kubectl config get-contexts -o name`.

    ~~~ shell
    $ kubectl config use-context <context-name> && \ 
    kubectl create secret generic movr-db-cert --from-file=cert=<full-path-to-cert> && \
    kubectl create secret generic movr-db-uri --from-literal=DB_URI="connection-string" && \
    kubectl create secret generic maps-api-key --from-literal=API_KEY="APIkey" \
    kubectl create -f ~/movr-flask/movr.yaml
    ~~~

    (Do this for each cluster context!)

1. Reserve s static IP address for the ingress.

    ~~~ shell
    $ gcloud compute addresses create --global movr-ip
    ~~~

1. Download [kubemci](https://github.com/GoogleCloudPlatform/k8s-multicluster-ingress) and make it executable.

    ~~~ shell
    $ chmod +x ~/kubemci
    ~~~

1. Use kubemci to make the ingress.

    ~~~ shell
    $ ~/kubemci create movr-mci \
    --ingress=<path>/movr-flask/mcingress.yaml \
    --gcp-project=<gcp_project> \
    --kubeconfig=<path>/mcikubeconfig
    ~~~

    **Note:** kubemci requires full paths.

1. In GCP's "Load balancing" console (found under "Network Services"), select and edit the load balancer that you just created. 

    1. Edit the backend configuration. 
        - Expand the advanced configurations, and add a custom header: `X-City: {client_city}`. This forwards an additional header to the application telling it what city the client is in. The header name (`X-City`) is hardcoded into the example application. 

    1. Edit the frontend configuration, and add a new frontend.
        - Under "Protocol", select HTTPS.
        - Under "IP address", select the static IP address that you reserved earlier (e.g., "movr-ip").
        - Under "Certificate", select "Create a new certificate".
        - In the "Create a new certificate" page, give a name to the certificate (e.g., "movr-ssl-cert"). Check "Create Google-managed certificate", and then under "Domains", enter a domain name that you own and want to use for your application.
    1. Review and finalize the load balancer, and then "Update".

    **Note:** It will take several minutes to provision the SSL certificate that you just created for the frontend.

1. Check the status of the ingress.

    ~~~ shell
    $ ~/kubemci list --gcp-project=<gcp_project>
    ~~~

1. In the GCP Cloud DNS console (under Network Services), create a new zone. You can name the zone whatever you want, but be sure to enter the same domain name for which you created a certificate earlier.

1. Select your zone, and copy the nameserver addresses (under "Data") for the recordset labeled "NS".

1. Add the nameserver addresses to the authorative nameserver list for your domain name, through your domain name provider.

    **Note:** It can take up to 48 hours for changes to the authorative nameserver list to take effect.

1. Navigate to the domain name and test out your application.

1. Clean up (at your leisure).
