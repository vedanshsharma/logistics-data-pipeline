import threading
from confluent_kafka import DeserializingConsumer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer
from confluent_kafka.serialization import StringDeserializer
from common.config import *
from common.mongodb_client import db

# Kafka configuration
kafka_config = {
    "bootstrap.servers": confluent_kafka_bootstrap_server,
    "sasl.mechanisms": "PLAIN",
    "security.protocol": "SASL_SSL",
    "sasl.username": confluent_kafka_api_key,
    "sasl.password": confluent_kafka_api_secret,
    "group.id": "CG1",
    "auto.offset.reset": "latest",
}

# Schema Registry client
schema_registry_client = SchemaRegistryClient(
    {
        "url": confluent_kafka_schema_registry_url,
        "basic.auth.user.info": "{}:{}".format(
            confluent_kafka_schema_registry_api_key,
            confluent_kafka_schema_registry_api_secret,
        ),
    }
)

# Fetch the latest Avro schema for the value
subject_name = "logistics-data-value"
schema_str = schema_registry_client.get_latest_version(subject_name).schema.schema_str

# Avro Deserializer for the value
key_deserializer = StringDeserializer("utf_8")
avro_deserializer = AvroDeserializer(schema_registry_client, schema_str)

# DeserializingConsumer
consumer = DeserializingConsumer(
    {
        "bootstrap.servers": kafka_config["bootstrap.servers"],
        "security.protocol": kafka_config["security.protocol"],
        "sasl.mechanisms": kafka_config["sasl.mechanisms"],
        "sasl.username": kafka_config["sasl.username"],
        "sasl.password": kafka_config["sasl.password"],
        "key.deserializer": key_deserializer,
        "value.deserializer": avro_deserializer,
        "group.id": kafka_config["group.id"],
        "auto.offset.reset": kafka_config["auto.offset.reset"],
        # 'enable.auto.commit': True,
        # 'auto.commit.interval.ms': 5000 # Commit every 5000 ms, i.e., every 5 seconds
    }
)
consumer.subscribe(["logistics-data"])


collection_name = "logistics_data"
collection = db[collection_name]

# Continually read messages from Kafka
try:
    while True:
        msg = consumer.poll(2.0)  # How many seconds to wait for message
        if msg is None:
            continue
        if msg.error():
            print("Consumer error: {}".format(msg.error()))
            continue
        #insert document into collection
        insert_result = collection.insert_one(msg.value())
        print(f"Document inserted with id: {insert_result.inserted_id}")

        print(
            "Successfully consumed record with key {}".format(
                msg.key()
            )
        )

except KeyboardInterrupt:
    pass
finally:
    consumer.close()
