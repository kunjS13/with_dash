import csv
import random
import datetime
import time

headers = ["TEAM ID", "TIME STAMPING", "PACKET COUNT", "ALTITUDE", "PRESSURE", "TEMP", "HUMIDITY", "VOLTAGE", "GNSS TIME", "GNSS LATITUDE", "GNSS LONGITUDE", "GNSS ALTITUDE", "GNSS SATS", "ACCELEROMETER DATA", "GYRO SPIN RATE", "FLIGHT SOFTWARE STATE", "ANY OPTIONAL DATA"]

packet_count = 0
max_packets = 100

while True:
    if packet_count >= max_packets:
        break
    
    team_id = "Team052"
    time_stamping = datetime.datetime.now().isoformat()
    packet_count += 1
    altitude = random.uniform(0, 10000)
    pressure = random.uniform(900, 1100)
    temp = random.uniform(-40, 40)
    humidity = random.uniform(0, 100)
    voltage = random.uniform(3.3, 5.0)
    gnss_time = datetime.datetime.now().isoformat()
    gnss_latitude = random.uniform(-90, 90)
    gnss_longitude = random.uniform(-180, 180)
    gnss_altitude = random.uniform(0, 10000)
    gnss_sats = random.randint(0, 30)
    accelerometer_data = (random.uniform(-10, 10), random.uniform(-10, 10), random.uniform(-10, 10))
    gyro_spin_rate = (random.uniform(-500, 500), random.uniform(-500, 500), random.uniform(-500, 500))
    flight_software_state = random.choice(['IDLE', 'FLIGHT', 'RECOVERY'])
    optional_data = "Optional data"

    with open(f'data/each_second/xbee_data_{packet_count}.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)

        writer.writerow([team_id, time_stamping, packet_count, altitude, pressure, temp, humidity, voltage, gnss_time, gnss_latitude, gnss_longitude, gnss_altitude, gnss_sats, accelerometer_data, gyro_spin_rate, flight_software_state, optional_data])

    time.sleep(1)