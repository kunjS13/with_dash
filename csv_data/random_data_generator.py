import csv
import time
import random
import os

# Define the field names
field_names = [
    "TEAM ID",
    "TIME STAMPING",
    "PACKET COUNT",
    "ALTITUDE",
    "PRESSURE",
    "TEMP",
    "HUMIDITY",
    "VOLTAGE",
    "GNSS TIME",
    "GNSS LATITUDE",
    "GNSS LONGITUDE",
    "GNSS ALTITUDE",
    "GNSS SATS",
    "ACCELEROMETER DATA",
    "GYRO SPIN RATE",
    "FLIGHT SOFTWARE STATE",
    "ANY OPTIONAL DATA",
]

file_exists = os.path.isfile("cansat_data.csv")

# Initialize the packet count
if file_exists:
    with open("cansat_data.csv", mode="r", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            last_packet_count = int(row["PACKET COUNT"])
            packet_count = last_packet_count  # Set packet_count to the last recorded count


# Create the CSV file and write the header if the file doesn't exist
with open("cansat_data.csv", mode="a", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=field_names)
    if not file_exists:
        writer.writeheader()

packet_count = 0  # Initialize the packet count

# Generate and append data to CSV file
while True:
    with open("cansat_data.csv", mode="a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=field_names)

        packet_count += 1  # Increment the packet count by 1

        # Generate random data for other fields
        data = {
            "TEAM ID": "Team052",
            "TIME STAMPING": time.strftime("%Y-%m-%d %H:%M:%S"),
            "PACKET COUNT": packet_count,
            "ALTITUDE": random.uniform(0, 10000),
            "PRESSURE": random.uniform(900, 1100),
            "TEMP": random.uniform(-20, 40),
            "HUMIDITY": random.uniform(0,100),
            "VOLTAGE": random.uniform(10, 14),
            "GNSS TIME": time.strftime("%H:%M:%S"),
            "GNSS LATITUDE": random.uniform(-90, 90),
            "GNSS LONGITUDE": random.uniform(-180, 180),
            "GNSS ALTITUDE": random.uniform(0, 5000),
            "GNSS SATS": random.randint(4, 12),
            "ACCELEROMETER DATA": random.uniform(-2, 2),
            "GYRO SPIN RATE": random.uniform(-200, 200),
            "FLIGHT SOFTWARE STATE": "Running",
            "ANY OPTIONAL DATA": "Optional",
        }

        writer.writerow(data)

    time.sleep(1)  # Generate data every second
