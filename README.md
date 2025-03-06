# logistics-data-pipeline
Logistics data pipeline using Kafka, MongoDB, and Avro, deployed with Docker and secured with GCP Secrets Manager.

# Logistic Data Pipeline

This project implements a data pipeline for processing and analyzing logistic data. It utilizes Docker and Docker Compose for containerization and orchestration, ensuring a consistent and reproducible environment.

## Project Structure
logistic-data-pipeline/
├── docker-compose.yml
├── Dockerfile
├── src/
│   ├── data_ingestion.py
│   ├── data_processing.py
│   ├── data_analysis.py
│   └── main.py
├── data/
│   ├── raw/
│   │   └── logistic_data.csv
│   └── processed/
├── README.md

* **`docker-compose.yml`**: Defines the services, networks, and volumes for the project.
* **`Dockerfile`**: Specifies the instructions for building the Docker image.
* **`src/`**: Contains the Python source code for the pipeline.
    * `data_ingestion.py`: Handles data ingestion from the raw data source.
    * `data_processing.py`: Performs data cleaning and transformation.
    * `data_analysis.py`: Executes data analysis and generates reports.
    * `main.py`: Orchestrates the entire pipeline.
* **`data/`**: Stores the raw and processed data.
    * `raw/`: Contains the original logistic data (`logistic_data.csv`).
    * `processed/`: Stores the processed data.
* **`README.md`**: This document.

## Prerequisites

* Docker: [Install Docker](https://docs.docker.com/get-docker/)
* Docker Compose: [Install Docker Compose](https://docs.docker.com/compose/install/)

## Getting Started

1.  **Clone the repository:**

    ```bash
    git clone <your_repository_url>
    cd logistic-data-pipeline
    ```

2.  **Build and run the Docker containers:**

    ```bash
    docker-compose up --build
    ```

    This command will:

    * Build the Docker image using the `Dockerfile`.
    * Start the container defined in `docker-compose.yml`.
    * Run the main.py file inside the container, which will execute the data pipeline.

3.  **View the processed data:**

    * The processed data will be stored in the `data/processed/` directory. You can inspect these files to see the results of the pipeline.

## Pipeline Description

The logistic data pipeline performs the following steps:

1.  **Data Ingestion:**
    * Reads the raw logistic data from `data/raw/logistic_data.csv`.
2.  **Data Processing:**
    * Cleans and transforms the data (e.g., handling missing values, data type conversions).
    * The processed data is saved to the `data/processed/` directory.
3.  **Data Analysis:**
    * Performs statistical analysis or generates reports based on the processed data.
    * Analysis results are saved or displayed.

## Customization

* **Data Source:**
    * To use a different data source, replace `data/raw/logistic_data.csv` with your own data file.
    * Modify `src/data_ingestion.py` to handle the new data format.
* **Data Processing and Analysis:**
    * Customize the data processing and analysis steps by modifying `src/data_processing.py` and `src/data_analysis.py`.
* **Docker Configuration:**
    * Adjust the Dockerfile and docker-compose.yml files to suit your specific requirements.
    * Add or remove python packages from the dockerfile as needed.
    * Adjust the context and dockerfile directives inside of the docker compose file if you change the location of your dockerfile.

## Cleaning Up

To stop and remove the containers:

```bash
docker-compose down
