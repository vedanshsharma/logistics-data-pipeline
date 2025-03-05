import datetime
from decimal import *
from time import sleep
from uuid import uuid4, UUID
import time
from datetime import datetime, timedelta
from confluent_kafka import SerializingProducer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
from confluent_kafka.serialization import StringSerializer
import random

from common.config import *


def delivery_report(err, msg):
    """
    Reports the failure or success of a message delivery.

    Args:
        err (KafkaError): The error that occurred on None on success.

        msg (Message): The message that was produced or failed.

    Note:
        In the delivery report callback the Message.key() and Message.value()
        will be the binary format as encoded by any configured Serializers and
        not the same object that was passed to produce().
        If you wish to pass the original object(s) for key and value to delivery
        report callback we recommend a bound callback or lambda where you pass
        the objects along.

    """
    if err is not None:
        print("Delivery failed for User record {}: {}".format(msg.key(), err))
        return
    print(
        "User record {} successfully produced to {} [{}] at offset {}".format(
            msg.key(), msg.topic(), msg.partition(), msg.offset()
        )
    )
    print("=====================")


kafka_config = {
    "bootstrap.servers": confluent_kafka_bootstrap_server,
    "sasl.mechanisms": "PLAIN",
    "security.protocol": "SASL_SSL",
    "sasl.username": confluent_kafka_api_key,
    "sasl.password": confluent_kafka_api_secret,
}

# Create a Schema Registry client
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
print("Schema from Registery---")
print(schema_str)
print("=====================")

# Create Avro Serializer for the value
key_serializer = StringSerializer("utf_8")
avro_serializer = AvroSerializer(schema_registry_client, schema_str)


# Define the SerializingProducer
producer = SerializingProducer(
    {
        "bootstrap.servers": kafka_config["bootstrap.servers"],
        "security.protocol": kafka_config["security.protocol"],
        "sasl.mechanisms": kafka_config["sasl.mechanisms"],
        "sasl.username": kafka_config["sasl.username"],
        "sasl.password": kafka_config["sasl.password"],
        "key.serializer": key_serializer,  # Key will be serialized as a string
        "value.serializer": avro_serializer,  # Value will be serialized as Avro
    }
)


def produce(num_rows=100):
    # Define possible values for categorical fields
    gps_providers = ["CONSENT TRACK", "OTHER GPS PROVIDER"]
    market_regular = ["Market", "Regular"]
    vehicle_types = ["Truck", "Tempo", "Car"]
    cities = ["Chennai", "Bengaluru", "Hyderabad", "Mumbai", "Pune"]
    states = ["Tamil Nadu", "Karnataka", "Telangana", "Maharashtra"]
    companies = ["Ashok Leyland", "Tata Motors", "Mahindra", "Maruti Suzuki"]
    materials = [
        "Engine Parts",
        "Car Chassis",
        "Electronics",
        "Textiles",
        "Food Grains",
    ]

    # Generate data rows
    data = []
    for i in range(num_rows):
        # Generate random values for each field
        gps_provider = random.choice(gps_providers)
        booking_id = f"MVCV{random.randint(1000000, 9999999)}/082021"
        market_reg = random.choice(market_regular)
        booking_date = int(
            (datetime.now() - timedelta(days=random.randint(1, 365))).timestamp() * 1000
        )
        vehicle_no = f"{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}{random.randint(10, 99)}{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}{random.randint(1000, 9999)}"
        origin_city = random.choice(cities)
        origin_state = random.choice(states)
        origin_location = f"{origin_city}, {origin_state}"
        dest_city = random.choice(cities)
        dest_state = random.choice(states)
        dest_location = f"{dest_city}, {dest_state}"
        org_lat = round(random.uniform(8.0, 37.0), 4)  # Latitude range for India
        org_lon = round(random.uniform(68.0, 97.0), 4)  # Longitude range for India
        org_lat_lon = f"{org_lat},{org_lon}"
        des_lat = round(random.uniform(8.0, 37.0), 4)
        des_lon = round(random.uniform(68.0, 97.0), 4)
        des_lat_lon = f"{des_lat},{des_lon}"
        data_ping_time = f"{random.randint(0, 23):02d}:{random.randint(0, 59):02d}.{random.randint(0, 9)}"
        planned_eta = f"{random.randint(1, 72):02d}:{random.randint(0, 59):02d}.{random.randint(0, 9)}"
        current_location = f"{random.choice(cities)}, {random.choice(states)}"
        actual_eta = int(
            (
                datetime.fromtimestamp(booking_date / 1e3)
                + timedelta(days=random.randint(1, 10))
            ).timestamp()
            * 1000
        )

        curr_lat = round(random.uniform(8.0, 37.0), 4)
        curr_lon = round(random.uniform(68.0, 97.0), 4)
        ontime = random.choice([True, False])
        delay = (
            random.randint(0, 360) if not ontime else 0
        )  # Delay in minutes if not on time
        origin_code = f"{origin_city[:3].upper()}{origin_state[:3].upper()}{random.randint(100, 999)}"
        dest_code = (
            f"{dest_city[:3].upper()}{dest_state[:3].upper()}{random.randint(100, 999)}"
        )
        trip_start_date = int(
            (
                datetime.fromtimestamp(booking_date / 1e3)
                + timedelta(days=random.randint(1, 23))
            ).timestamp()
            * 1000
        )
        trip_end_date = int(
            (
                datetime.fromtimestamp(booking_date / 1e3)
                + timedelta(days=random.randint(1, 23))
            ).timestamp()
            * 1000
        )
        distance = random.randint(100, 1000)
        vehicle_type = random.choice(vehicle_types)
        min_kms = random.randint(300, 600)
        driver_name = f"Driver {random.randint(1, 100)}"
        driver_mobile = f"+91-{random.randint(9000000000, 9999999999)}"
        customer_id = f"CUST{random.randint(1000, 9999)}"
        customer_name = random.choice(companies)
        supplier_id = f"SUPP{random.randint(1000, 9999)}"
        supplier_name = f"{random.choice(['ABC', 'XYZ', 'PQR'])} Logistics"
        material_shipped = random.choice(materials)

        # Create a data row
        data = {
            "GpsProvider": gps_provider,
            "BookingID": booking_id,
            "Market_Regular": market_reg,
            "BookingID_Date": booking_date,
            "vehicle_no": vehicle_no,
            "Origin_Location": origin_location,
            "Destination_Location": dest_location,
            "Org_lat_lon": org_lat_lon,
            "Des_lat_lon": des_lat_lon,
            "Data_Ping_time": data_ping_time,
            "Planned_ETA": planned_eta,
            "Current_Location": current_location,
            "DestinationLocation": dest_location,
            "actual_eta": actual_eta,
            "Curr_lat": curr_lat,
            "Curr_lon": curr_lon,
            "ontime": ontime,
            "delay": delay,
            "OriginLocation_Code": origin_code,
            "DestinationLocation_Code": dest_code,
            "trip_start_date": trip_start_date,
            "trip_end_date": trip_end_date,
            "TRANSPORTATION_DISTANCE_IN_KM": distance,
            "vehicleType": vehicle_type,
            "Minimum_kms_to_be_covered_in_a_day": min_kms,
            "Driver_Name": driver_name,
            "Driver_MobileNo": driver_mobile,
            "customerID": customer_id,
            "customerNameCode": customer_name,
            "supplierID": supplier_id,
            "supplierNameCode": supplier_name,
            "Material_Shipped": material_shipped,
        }
        producer.produce(
            topic="logistics-data",
            key=str(uuid4()),
            value=data,
            on_delivery=delivery_report,
        )
        producer.flush()
        time.sleep(2)


print(produce(2))
