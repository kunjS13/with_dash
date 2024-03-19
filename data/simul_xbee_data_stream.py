import csv
import random
import datetime
import time
import os
import pytz

# headers_0 = [ #ideal headers
#     "TEAM_ID",
#     "PACKET_COUNT",
#     "FLIGHT_SOFTWARE_STATE",
#     "GPS_TIME",
#     "GPS_LATITUDE",
#     "GPS_LONGITUDE",
#     "GPS_ALTITUDE",
#     "GPS_SATS",
#     "ACCELEROMETER_X",
#     "ACCELEROMETER_Y",
#     "ACCELEROMETER_Z",
#     "GYRO_X",
#     "GYRO_Y",
#     "GYRO_Z",
#     "MAGNETOMETER_X",
#     "MAGNETOMETER_Y",
#     "MAGNETOMETER_Z",
#     "GYRO_SPIN_RATE",
#     "ALTITUDE",
#     "PRESSURE",
#     "TEMP",
#     "HUMIDITY",
#     "VOLTAGE",
#     "TEMPERATURE",
#     "BATTERY_VOLTAGE",
#     "CURRENT",
#     "POWER",
# ]

headers_1 = [ #current headers
    "TEAM_ID",
    "PACKET_COUNT",
    "EC_STATE",
    "GNSS_HOUR",
    "GNSS_MINUTE",
    "GNSS_SECOND",
    "ORIENTATION_X",
    "ORIENTATION_Y",
    "ORIENTATION_Z",
    "ACCEL_X",
    "ACCEL_Y",
    "ACCEL_Z",
    "GYRO_X",
    "GYRO_Y",
    "GYRO_Z",
    "TEMPERATURE",
    "BMP_ALTITUDE",
    "BMP_PRESSURE",
    "GNSS_LATITUDE",
    "GNSS_LONGITUDE",
    "GNSS_ALTITUDE",
]

now = datetime.datetime.now()
gmt_time = pytz.timezone('GMT').localize(now)

packet_count = 0
max_packets = 100

while True:
    if packet_count >= max_packets:
        break

    if os.path.exists(f"data/each_second/xbee_data_100.csv"):
        print("File 'xbee_data_100.csv' already exists. Exiting.")
        break

    team_id = "Team052"
    # time_stamping = datetime.datetime.now().isoformat()
    packet_count += 1
    ec_state = "IDLE"
    gnss_hour = gmt_time.hour
    gnss_minute = gmt_time.minute
    gnss_second = gmt_time.second
    orientation_x = random.uniform(0, 360)
    orientation_y = random.uniform(0, 360)
    orientation_z = random.uniform(0, 360)
    accel_x = random.uniform(10, 20)
    accel_y = random.uniform(10, 20)
    accel_z = random.uniform(10, 20)
    gyro_x = random.uniform(0,5)
    gyro_y = random.uniform(0,5)
    gyro_z = random.uniform(0,5)
    temperature = random.uniform(0, 40)
    bmp_altitude = random.uniform(0, 100)
    bmp_pressure = random.uniform(100000, 110000)
    gnss_latitude = random.uniform(-90, 90)
    gnss_longitude = random.uniform(-180, 180)
    gnss_altitude = random.uniform(0, 10000)
    # accelerometer_data = (
    #     random.uniform(-10, 10),
    #     random.uniform(-10, 10),
    #     random.uniform(-10, 10),
    # )
    # gyro_spin_rate = (
    #     random.uniform(-500, 500),
    #     random.uniform(-500, 500),
    #     random.uniform(-500, 500),
    # )
    # flight_software_state = random.choice(["IDLE", "FLIGHT", "RECOVERY"])
    

    with open(
        f"data/each_second/xbee_data_{packet_count}.csv", "w", newline=""
    ) as file:
        writer = csv.writer(file)
        writer.writerow(headers_1)

        writer.writerow(
            [
                team_id,
                packet_count,
                ec_state,
                gnss_hour,
                gnss_minute,
                gnss_second,
                orientation_x,
                orientation_y,
                orientation_z,
                accel_x,
                accel_y,
                accel_z,
                gyro_x,
                gyro_y,
                gyro_z,
                temperature,
                bmp_altitude,
                bmp_pressure,
                gnss_latitude,
                gnss_longitude,
                gnss_altitude,
            ]
        )
        print(team_id,
                packet_count,
                ec_state,
                gnss_hour,
                gnss_minute,
                gnss_second,
                orientation_x,
                orientation_y,
                orientation_z,
                accel_x,
                accel_y,
                accel_z,
                gyro_x,
                gyro_y,
                gyro_z,
                temperature,
                bmp_altitude,
                bmp_pressure,
                gnss_latitude,
                gnss_longitude,
                gnss_altitude)
        
    time.sleep(1)
