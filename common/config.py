from google.cloud import secretmanager
from google.auth import default


def get_project_id():
    """Gets the project ID from the default credentials."""
    credentials, project = default()
    if project:
        return project
    else:
        # Fallback in case default credentials don't have project ID
        # (e.g., local testing without gcloud auth)
        print("Warning: Could not automatically determine project ID.")
        return None


def access_secret_version(secret_id, version_id="latest"):
    """Access the payload for the given secret version if one exists."""
    client = secretmanager.SecretManagerServiceClient()
    if project_id is None:
        print("Project ID is none, secret access will fail")
        return None
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    try:
        response = client.access_secret_version(request={"name": name})
        return response.payload.data.decode("UTF-8")
    except Exception as e:
        print(f"Error accessing secret {secret_id}: {e}")
        return None


# Example usage within your config.py:
project_id = get_project_id()
if project_id:
    print(f"Project ID: {project_id}")
else:
    print("Project ID is not available")


confluent_kafka_api_key = access_secret_version("confluent-kafka-api-key")
confluent_kafka_api_secret = access_secret_version("confluent-kafka-api-secret")
confluent_kafka_bootstrap_server = access_secret_version(
    "confluent-kafka-bootstrap-server"
)
confluent_kafka_schema_registry_api_key = access_secret_version(
    "confluent-kafka-schema-registry-api-key"
)
confluent_kafka_schema_registry_api_secret = access_secret_version(
    "confluent-kafka-schema-registry-api-secret"
)
confluent_kafka_schema_registry_url = access_secret_version(
    "confluent-kafka-schema-registry-url"
)
mongodb_connection_str = access_secret_version("mongodb-connection-str")
