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

    So, create a file named `.env`, and then define the connection string in that file as the `DEBUG_URI` environment variables. Note that for SQLAlchemy, the connection string protocol needs to be specific to the CockroachDB dialect.

    For example:

    ~~~
    DEBUG_URI = 'cockroachdb://root@127.0.0.1:52382/movr'
    ~~~

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

1. Navigate to the URL provided.

## Multi-region Deployment

### Database Deployment (Cockroach Cloud)

To deploy CockroachDB, we recommend that you use [Cockroach Cloud](https://cockroachlabs.cloud).

1. Create a multi-region CockroachCloud cluster, with GCP, in regions us-west1, us-east1, europe-west1.
1. After you create the CC cluster, create a user and network, and then copy the connection string, with the user and password specified. See https://www.cockroachlabs.com/docs/cockroachcloud/stable/cockroachcloud-connect-to-your-cluster.html for instructions.
1. Download the cert.
1. Copy the cert to `movr/certs/ca.crt`.
1. Open a separate terminal and run the `dbinit.sql` file on the running cluster to initialize the database.
    ~~~ shell
    $ cockroach sql --url ‘connection_string’ < dbinit.sql
    ~~~
    **Note:** You need to specify the password in the connection string!
    e.g.
    ~~~ shell
    $ cockroach sql --url \ 'postgresql://user:password@region.cockroachlabs.cloud:26257/defaultdb?sslmode=verify-full&sslrootcert=certs/ca.crt' < dbinit.sql
    ~~~

**Note:** You can also deploy CRDB manually. For instructions, see the [Manual Deployment](manual-deployment.html) page of the Cockroach Labs documentation site.

### Application Deployment

1. Create a glcoud account at https://cloud.google.com/.
1. Create a gcloud project on the [GCP console](https://console.cloud.google.com/).
1. Enable the Google Maps API, and retrieve the API key from https://console.cloud.google.com/apis/library. 
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
1. Open the template Dockerfile, and set ENV variables to match your environment.
    - API_KEY to your google maps API key.
    - DB_URI to the connection string, but make sure cockroachdb is the protocol and not postgres.
1. Build and run the docker image locally.
    ~~~ shell
    $ docker build -t gcr.io/<gcp_project>/movr-app:v1 .
    $ docker run --publish 8080:8080 gcr.io/<gcp_project>/movr-app:v1
    ~~~
    e.g.
    ~~~ shell
    $ docker build -t gcr.io/movr-test-259013/movr-app:v1 .
    $ docker run --publish 8080:8080 gcr.io/movr-test-259013/movr-app:v1
    ~~~
1. Navigate to http://localhost:8080.
    Note: The homepage will show an error because you are connecting with a localhost IP. It still connects to the database, using New York as the city. 
1. Push the Docker image to the project’s gcloud container registry. 
    ~~~ shell
    $ docker push gcr.io/movr-test-259013/movr-app:v1
    ~~~
1. Create a K8s cluster for all three regions.
    ~~~ shell
    $ gcloud config set compute/zone us-east1-b
    $ gcloud container clusters create movr-us-east
    $ gcloud config set compute/zone us-west1-b
    $ gcloud container clusters create movr-us-west
    $ gcloud config set compute/zone europe-west1-b
    $ gcloud container clusters create movr-europe-west
    ~~~
1. Add container credentials to kubeconfig.
    ~~~ shell
    $ KUBECONFIG=~/mcikubeconfig gcloud container clusters get-credentials --zone=us-east1-b movr-us-east
    $ KUBECONFIG=~/mcikubeconfig gcloud container clusters get-credentials --zone=us-west1-b movr-us-west
    $ KUBECONFIG=~/mcikubeconfig gcloud container clusters get-credentials --zone=europe-west1-b movr-europe-west
    ~~~
1. Create the deployment and service for each context, using the movr.yaml manifest file.
    ~~~ shell
    $ for ctx in $(kubectl config get-contexts -o name); do kubectl --context="${ctx}" create -f ~/movr/movr.yaml; done
    ~~~
1. Reserve static IP for ingress.
    ~~~ shell
    $ gcloud compute addresses create --global movr-ip
    ~~~
1. Download [kubemci](https://github.com/GoogleCloudPlatform/k8s-multicluster-ingress).
    ~~~ shell
    $ chmod +x ~/kubemci
    ~~~
1. Create the ingress.
    ~~~ shell
    $ ~/kubemci create movr-mci \
    --ingress=~/movr-flask/mcingress.yaml \
    --gcp-project=movr-test-259013 \
    --kubeconfig=~/mcikubeconfig
    ~~~

    **Note:** kubemci requires full paths.
1. In the GCP load balancer console, edit the load balancer that you just created. Then edit the backend configuration. Expand the advanced configurations, add a custom header: `X-City: {client_city}`. This forwards an additional header to the application telling it what city the client is in.
1. Check the status of the ingress
    ~~~ shell
    $ ~/kubemci list --gcp-project=movr-test-259013
    ~~~
1. Navigate to the IP listed for the ingress (using HTTP!).
1. Clean up (at your leisure).
