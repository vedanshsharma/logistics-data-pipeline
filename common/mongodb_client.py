from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from .config import mongodb_connection_str

# mongodb connetion string
conn_string = mongodb_connection_str
# Connect to MongoDB
database_name = "logistics_data"
db = None
try:
    client = MongoClient(conn_string)
    client.admin.command("ping")  # Test the connection
    print("Connected to MongoDB!")
    db = client[database_name]
except ConnectionFailure as e:
    print(f"Failed to connect to MongoDB: {e}")
except Exception as e:  # Catch other exceptions
    print(f"An unexpected error occurred during MongoDB connection: {e}")