# Logistics Data Pipeline

This project implements a data pipeline for processing logistics events. It consists of a producer, a consumer, and an API.

## Architecture


The pipeline follows these steps:

1.  **Producer:** Generates simulated logistics events and publishes them to a Kafka topic.
2.  **Consumer:** Consumes the events from the Kafka topic and stores them in a MongoDB database.
3.  **API:** Provides endpoints to retrieve and query the logistics data from MongoDB.

## Prerequisites

* Google Cloud Platform (GCP) account
* `gcloud` CLI installed and configured
* Docker and Docker Compose installed
* MongoDB Atlas account (or a self-hosted MongoDB instance)
* Confluent Cloud account (or a self-hosted Kafka cluster)

## Setup

1.  **GCP Secrets Manager:**
    * Create a GCP project.
    * Enable the Secrets Manager API.
    * Create secrets for your Confluent Cloud API key and secret:
        * Navigate to "Secrets Manager" in the GCP Console.
        * Click "Create Secret".
        * Enter a secret name (e.g., `CONFLUENT_API_KEY`).
        * Enter the secret value (your Confluent Cloud API key).
        * Repeat for `CONFLUENT_API_SECRET`.
    * Grant the service account that will be used by the docker containers the "Secret Manager Secret Accessor" role.

2.  **Service Account Key File:**
    * Create a service account in the GCP Console (IAM & Admin > Service Accounts).
    * Download the service account JSON key file (`gcp-sa.json`).
    * Place the `gcp-sa.json` file in the root directory of the project. **Never commit this file to version control.**

3.  **MongoDB Setup:**
    * Create a MongoDB database.
    * Obtain your MongoDB connection URI.
    * Set the `MONGODB_URI` and `MONGODB_DATABASE` variables inside of `common/config.py`.

4.  **Confluent Cloud Setup:**
    * Create a Confluent Cloud account.
    * Create a Kafka cluster.
    * Create a Kafka topic.
    * Obtain your Kafka bootstrap servers.
    * Set the `KAFKA_BOOTSTRAP_SERVERS` variable inside of `common/config.py`.

5.  **Environment Configuration:**
    * Open `common/config.py` and set the following variables:
        * `MONGODB_URI`: Your MongoDB connection URI.
        * `MONGODB_DATABASE`: Your MongoDB database name.
        * `KAFKA_BOOTSTRAP_SERVERS`: Your Confluent Cloud Kafka bootstrap servers.
        * `KAFKA_TOPIC`: Your Kafka topic name.

6.  **Build and Run:**
    * From the project root directory, run:

        ```bash
        docker-compose up --build -d
        ```

    * This will build and start the producer, consumer, and API containers.

## Using the API

* The API is accessible at `http://localhost:8000`.
* API documentation is available at `http://localhost:8000/docs`.

### API Endpoints

* **GET /logistics/events/**: Retrieves all logistics events. Supports query parameters for filtering:
    * `order_id`: Filter by order ID.
    * `location`: Filter by location.
    * `status`: Filter by status.
    * `start_timestamp`: Filter by start timestamp.
    * `end_timestamp`: Filter by end timestamp.
* **GET /logistics/events/{order_id}**: Retrieves events for a specific order ID.

### Example curl request

```bash
curl "http://localhost:8000/logistics/events/?location=New%20York&status=Shipped"