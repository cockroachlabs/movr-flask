# MovR

## Overview

This repo contains the source code for an example implementation of a multi-region application for the fictional vehicle-sharing company [MovR](https://www.cockroachlabs.com/docs/dev/movr.html).

The application stack consists of the following components:

- A multi-node, geo-distributed CockroachDB cluster, with each node's locality corresponding to cloud provider regions.
- A geo-partitioned database schema that defines the tables and indexes for user, vehicle, and ride data.
- Python class definitions that map to the tables in our database.
- A backend API that defines the application's connection to the database and the database transactions.
- A Flask server that handles requests from client web browsers.
- HTML files that define web pages that the Flask server renders.

## Requirements

Make sure that you have installed the following on your local machine:

- [CockroachDB](https://www.cockroachlabs.com/docs/stable/install-cockroachdb-mac.html/install-cockroachdb-mac.html)
- [Python 3](https://www.python.org/downloads/)
- [`pipenv`](https://docs.pipenv.org/en/latest/install/#installing-pipenv) (for debugging)
- [Google Cloud SDK](https://cloud.google.com/sdk/install) (for production deployments)
- [Docker](https://docs.docker.com/v17.12/docker-for-mac/install/) (for production deployments)
- [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/) (for production deployments)

There are a number of Python libraries that you also need to run the application, including `flask`, `sqlalchemy`, and `cockroachdb`. Rather than downloading these dependencies directly from PyPi to your machine, you should list them in dependency configuration files (see [Debugging][#debugging] and [Multi-region deployment][#multi-region-deployment] for examples).

## Debugging

### Database set-up

In production, you want to start a secure CockroachDB cluster, with nodes on machines located in different areas of the world. For debugging purposes, you can just use the [`cockroach demo`](https://www.cockroachlabs.com/docs/stable/cockroach-demo.html) command. This command starts up an insecure, virtual nine-node cluster.

1. Run `cockroach demo`, with the `--nodes` and `--demo-locality` flags. The database schema provided in this repo assumes the [GCP region names](https://cloud.google.com/about/locations/). 

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

1. In a separate terminal window, run the following command to load `dbinit.sql` (located at the top level of the repo) to the demo database:

    ~~~ shell
    $ cockroach sql --insecure --url='postgresql://root@127.0.0.1:<some_port>/movr' < dbinit.sql
    ~~~

### Application set-up

In production, you probably want to containerize your application and deploy it with k8s. For debugging, use [`pipenv`](https://pypi.org/project/pipenv/), a tool that includes `pip` (to make dependencies) and `virtualenv` (to create virtual environments).

1. Run the following command to initialize the project's virtual environment:

    ~~~ shell
    $ pipenv --three
    ~~~

    `pipenv` creates a `Pipfile` in the current directory. Open this `Pipfile`, and edit it to read as follows:

    ~~~ toml
    [[source]]
    name = "pypi"
    url = "https://pypi.org/simple"
    verify_ssl = true

    [dev-packages]

    [packages]
    cockroachdb = "*"
    psycopg2-binary = "*"
    SQLAlchemy = "*"
    SQLAlchemy-Utils = "*"
    Flask = "*"
    Flask-SQLAlchemy = "*"
    Flask-WTF = "*"
    Flask-Bootstrap = "*"
    Flask-Login = "*"
    WTForms = "*"
    gunicorn = "*"
    geopy = "*"

    [requires]
    python_version = "3.7"
    ~~~

1. Run the following command to install the packages listed in the `Pipfile`:

    ~~~ shell
    $ pipenv install
    ~~~

1. Pipenv automatically sets any variables defined in a `.env` file as environment variables in a Pipenv virtual environment. To connect to a SQL database (like CockroachDB) from a client, you need a [SQL connection string](https://en.wikipedia.org/wiki/Connection_string).

    So, open the `.env`, and then define the `DB_URI` environment variable as the connection string for the demo cluster that you started earlier. In SQLAlchemy, the connection string protocol needs to be specific to the CockroachDB dialect.

    For example:

    ~~~
    DB_URI = 'cockroachdb://root@127.0.0.1:52382/movr'
    ~~~

    You can also specify other variables in this file that you'd rather not hard-code in the application, like API keys and secret keys used by the application. For debugging purposes, you should leave these variables as they are.

1. Activate the virtual environment:

    ~~~ shell
    $ pipenv shell
    ~~~

    The prompt should now read `~bash-3.2$`. From this shell, you can run any Python3 application with the required dependencies that you listed in the `Pipfile`, and the environment variables that you listed in the `.env` file. You can exit the shell subprocess at any time with a simple `exit` command.

1. To test out the application, you can simply run the server file:

    ~~~ shell
    $ python3 server.py
    ~~~

    You can alternatively use [gunicorn](https://gunicorn.org/).

    ~~~ shell
    $ gunicorn -b localhost:8000 server:app
    ~~~

1. Navigate to the URL provided to test out the application.

## Multi-region Deployment

### Database Deployment (CockroachCloud)

In production, you want to start a secure CockroachDB cluster, with nodes on machines located in different areas of the world. 

To deploy CockroachDB in multiple regions, using [CockroachCloud](https://cockroachlabs.cloud):

1. Create a CockroachCloud account.

1. Request a multi-region CockroachCloud cluster on GCP, in regions `us-west1`, `us-east1`, and `europe-west1`.

1. After the cluster is created, open the console, and select the cluster.

1. Select **SQL Users** from the side panel, select **Add user**, give the user a name and a password, and then add the user. You can use any user name except "root".

1. Select **Networking** from the side panel, and then select **Add network**. Give the network any name you'd like, select either a **New network** or a **Public network**, check both **UI** and **SQL**, and then add the network. In this example, we use a public network.

1. Select **Connect** at the top-right corner of the cluster console.

1. Select the **User** that you created, and then **Continue**.

1. Copy the connection string, with the user and password specified.

1. **Go back**, and retrieve the connection strings for the other two regions.

1. Download the cluster cert to your local machine (it's the same for all regions).

1. Open a new terminal, and run the `dbinit.sql` file on the running cluster to initialize the database. You can connect to the database from any node on the cluster for this step.

    ~~~ shell
    $ cockroach sql --url any-connection-string < dbinit.sql
    ~~~


    **Note:** You need to specify the password in the connection string!

    e.g.,
    ~~~ shell
    $ cockroach sql --url \ 'postgresql://user:password@region.cockroachlabs.cloud:26257/defaultdb?sslmode=verify-full&sslrootcert=certs-dir/movr-app-ca.crt' < dbinit.sql
    ~~~


**Note:** You can also deploy CRDB manually. For instructions, see the [Manual Deployment](https://www.cockroachlabs.com/docs/stable/manual-deployment.html) page of the Cockroach Labs documentation site.

### Application Deployment

To deploy the application globally, we recommend that you use a major cloud provider with a global load-balancing service and a Kubernetes engine. For our deployment, we use GCP. 

**Note:** To serve a secure web application that takes HTTPS requests, you also need a public domain name! SSL certificates are not assigned to IP addresses.

1. If you don't have a glcoud account, create one at https://cloud.google.com/.

1. Create a gcloud project on the [GCP console](https://console.cloud.google.com/).

1. **Optional:** Enable the [Google Maps Embed API](https://console.cloud.google.com/apis/library), create an API key, restrict the API key to all subdomains of your domain name (e.g. `https://site.com/*`), and retrieve the API key. 

    **Note:** The example HTML templates include maps. Not providing an API key to the application will not break the application.

1. Configure/authorize the `gcloud` CLI to use your project and region.

    ~~~ shell
    $ gcloud init
    $ gcloud auth login
    $ gcloud auth application-default login
    ~~~

1. If you haven't already, install `kubectl`.

    ~~~ shell
    $ gcloud components install kubectl
    ~~~

1. Build and run the Docker image locally.

    ~~~ shell
    $ docker build -t gcr.io/<gcp_project>/movr-app:v1 .
    ~~~

    If there are no errors, the container built successfully.

1. Push the Docker image to the project’s gcloud container registry.

    e.g.,
    ~~~ shell
    $ docker push gcr.io/<gcp_project>/movr-app:v1
    ~~~

1. Create a K8s cluster in each region.

    ~~~ shell
    $ gcloud config set compute/zone us-east1-b && \
      gcloud container clusters create movr-us-east
    $ gcloud config set compute/zone us-west1-b && \
      gcloud container clusters create movr-us-west
    $ gcloud config set compute/zone europe-west1-b && \
      gcloud container clusters create movr-europe-west
    ~~~

1. Add the container credentials to `kubeconfig`.

    ~~~ shell
    $ KUBECONFIG=~/mcikubeconfig gcloud container clusters get-credentials --zone=us-east1-b movr-us-east
    $ KUBECONFIG=~/mcikubeconfig gcloud container clusters get-credentials --zone=us-west1-b movr-us-west
    $ KUBECONFIG=~/mcikubeconfig gcloud container clusters get-credentials --zone=europe-west1-b movr-europe-west
    ~~~

1. For each cluster context, create a secret for the connection string, Google Maps API (optional), and the certs, and then create the k8s deployment and service using the `movr.yaml` manifest file. To get the context for the cluster, run `kubectl config get-contexts -o name`.

    ~~~ shell
    $ kubectl config use-context <context-name> && \ 
    kubectl create secret generic movr-db-cert --from-file=cert=<full-path-to-cert> && \
    kubectl create secret generic movr-db-uri --from-literal=DB_URI="connection-string" && \
    kubectl create secret generic maps-api-key --from-literal=API_KEY="APIkey" \
    kubectl create -f ~/movr-flask/movr.yaml
    ~~~

    **Note:** You need to do this for each cluster context!

1. Reserve a static IP address for the ingress.

    ~~~ shell
    $ gcloud compute addresses create --global movr-ip
    ~~~

1. Download [`kubemci`](https://github.com/GoogleCloudPlatform/k8s-multicluster-ingress), and then make it executable.

    ~~~ shell
    $ chmod +x ~/kubemci
    ~~~

1. Use `kubemci` to make the ingress.

    ~~~ shell
    $ ~/kubemci create movr-mci \
    --ingress=<path>/movr-flask/mcingress.yaml \
    --gcp-project=<gcp_project> \
    --kubeconfig=<path>/mcikubeconfig
    ~~~

    **Note:** `kubemci` requires full paths.

1. In GCP's **Load balancing** console (found under **Network Services**), select and edit the load balancer that you just created. 

    1. Edit the backend configuration. 
        - Expand the advanced configurations, and add [a custom header](https://cloud.google.com/load-balancing/docs/user-defined-request-headers): `X-City: {client_city}`. This forwards an additional header to the application telling it what city the client is in. The header name (`X-City`) is hardcoded into the example application. 

    1. Edit the frontend configuration, and add a new frontend.
        - Under "**Protocol**", select HTTPS.
        - Under "**IP address**", select the static IP address that you reserved earlier (e.g., "`movr-ip`").
        - Under "**Certificate**", select "**Create a new certificate**".
        - On the "**Create a new certificate**" page, give a name to the certificate (e.g., "`movr-ssl-cert`"), check "**Create Google-managed certificate**", and then under "Domains", enter a domain name that you own and want to use for your application.
    1. Review and finalize the load balancer, and then "**Update**".

    **Note:** It will take several minutes to provision the SSL certificate that you just created for the frontend.

1. Check the status of the ingress.

    ~~~ shell
    $ ~/kubemci list --gcp-project=<gcp_project>
    ~~~

1. In the **Cloud DNS** console (found under **Network Services**), create a new zone. You can name the zone whatever you want. Enter the same domain name for which you created a certificate earlier.

1. Select your zone, and copy the nameserver addresses (under "**Data**") for the recordset labeled "**NS**".

1. Outside of the GCP console, through your domain name provider, add the nameserver addresses to the authorative nameserver list for your domain name.

    **Note:** It can take up to 48 hours for changes to the authorative nameserver list to take effect.

1. Navigate to the domain name and test out your application.

1. Clean up (at your leisure).
