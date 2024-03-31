<h1 align="center">
Retrival Augmented Generation(RAG) based Chat Agent for Data Analysis and Insights
</h1>

## Features

- RAG for CSV files, enabling robust and vivid data analysis via LLMS.
- A QA Chatbot to query and get insigths on any kind of data
- Containerized the app using Docker
- Deployment on Google Cloud using [Cloud Run](https://cloud.google.com/sdk/gcloud/reference/run/deploy)
- CI/CD using Github Actions

## 💻 Running Locally

1. Clone the repository📂

```bash
git clone https://github.com/sudarshan-koirala/langchain-chainlit-docker-deployment
cd RAG_Data_Analysis_Chatbot
```

2. Install dependencies with [Poetry](https://python-poetry.org/) and activate virtual environment🔨  

To install Poetry, run the following command, `pipx install poetry`. Make sure pipx is installed in your machine.  

```bash
poetry install
poetry shell
```

3. Run the Chainlit server🚀

```bash
chainlit run demo_app/main.py
```

##  Run App using Docker
This project includes `Dockerfile` to run the app in Docker container.

Build the docker container

``DOCKER_BUILDKIT=1 docker build --target=runtime . -t langchain-chainlit-chat-app:latest
``

Run the docker container using docker-compose

``docker-compose up``


☁️ Deploy App on Google Cloud using Cloud Run
--------------------------------
This app can be deployed on Google App Engine following below steps.

Two configurations files shown below are used. 

1. `app.yaml`: A Configuration file for `gcloud`
2. `.gcloudignore` : Configure the file to ignore file / folders to be uploaded

`Dockerfile` is used to deploy the app on GCP.

### Before using gcloud, you need to install gcloud cli if you haven't already
- For me as I am in github codespace, I follow these [instructions](https://cloud.google.com/sdk/docs/install#linux), Choose the one that fits your machine.
- Once you installed, in order to use `gcloud` instead of `./google-cloud-sdk/bin/gcloud`, you need to add it to the path.
- For me, its zsh so, follow these steps.
```
1. vim ~/.zshrc

# Add this line at the end of the file, replacing [PATH_TO_GCLOUD] with the absolute path to your google-cloud-sdk/bin/ directory

2. export PATH="$PATH:[PATH_TO_GCLOUD]/google-cloud-sdk/bin/"

Save and close. To make these changes take effect, you need to source your ~/.zshrc file

3. source ~/.zshrc

```

## Main steps to Deploy 🚀

1. **Initialise & Configure the App**

First create a project in [GCP console](https://console.cloud.google.com)

```
gcloud auth login
gcloud auth list
gcloud app create --project=[YOUR_PROJECT_ID]
gcloud config set project [YOUR_PROJECT_ID]
```

Provide billing account for this project by running `gcloud beta billing accounts list` OR you can do it manually from the GCP console.


2. **Enable Services for the Project**: We have to enable services for Cloud Run using below set of commands
```
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
```

3. **Create Service Accounts with Permissions**
```
gcloud iam service-accounts create langchain-app-cr \
    --display-name="langchain-app-cr"

gcloud projects add-iam-policy-binding langchain-cl-chat-with-csv \
    --member="serviceAccount:langchain-app-cr@langchain-chat.iam.gserviceaccount.com" \
    --role="roles/run.invoker"

gcloud projects add-iam-policy-binding langchain-cl-chat-with-csv \
    --member="serviceAccount:langchain-app-cr@langchain-chat.iam.gserviceaccount.com" \
    --role="roles/serviceusage.serviceUsageConsumer"

gcloud projects add-iam-policy-binding langchain-cl-chat-with-csv \
    --member="serviceAccount:langchain-app-cr@langchain-chat.iam.gserviceaccount.com" \
    --role="roles/run.admin"
```

4. **Check the artifacts location**
```
gcloud artifacts locations list
```
5. **Generate Docker with Region**
```
DOCKER_BUILDKIT=1 docker build --target=runtime . -t europe-west6-docker.pkg.dev/langchain-cl-chat-with-csv/clapp/langchain-chainlit-chat-app:latest
```

6. **Push Docker to Artifacts Registry**
```
# Create a repository clapp
gcloud artifacts repositories create clapp \
    --repository-format=docker \
    --location=europe-west6 \
    --description="A Langachain Chainlit App" \
    --async
# Assign authuntication
gcloud auth configure-docker europe-west6-docker.pkg.dev

# Push the Container to Repository
docker images
docker push europe-west6-docker.pkg.dev/langchain-chat/clapp/langchain-chainlit-chat-app:latest
```

7. **Deploy the App using Cloud Run**

```
gcloud run deploy langchain-cl-chat-with-csv-app --image=europe-west6-docker.pkg.dev/langchain-cl-chat-with-csv/clapp/langchain-chainlit-chat-app:latest \
    --region=europe-west6 \
    --service-account=langchain-app-cr@langchain-cl-chat-with-csv.iam.gserviceaccount.com \
    --port=8000
```

3. **Access the App** 
Once deployed, you can try the app similar to follwing link. I have deleted the app for cost saving as I genrally use it locally.

https://langchain-cl-chat-with-csv-app-iu7ux3rrza-ez.a.run.app/

