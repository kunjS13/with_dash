import pandas as pd
import time

# Read the main CSV file
main_file = 'cansat_data.csv'  # Replace with the path to your main CSV file
df = pd.read_csv(main_file)

# Create dataframes for each set of columns
gnss_coords = df[['GNSS LATITUDE', 'GNSS LONGITUDE']]
gnss_altitude_time = df[['GNSS ALTITUDE', 'GNSS TIME']]
gnss_time_timestamp = df[['GNSS TIME', 'TIME STAMPING']]
temp_timestamp = df[['TEMP', 'TIME STAMPING']]
alt_pressure_timestamp = df[['ALTITUDE', 'PRESSURE', 'TIME STAMPING']]
humidity_timestamp = df[['HUMIDITY', 'TIME STAMPING']]
gyro_timestamp = df[['GYRO SPIN RATE', 'TIME STAMPING']]
voltage_timestamp = df[['VOLTAGE', 'TIME STAMPING']]

# Save each dataframe to a separate CSV file with descriptive names
while True:
    gnss_coords.to_csv('gnss_coordinates.csv', index=False)
    gnss_altitude_time.to_csv('gnss_altitude_time.csv', index=False)
    gnss_time_timestamp.to_csv('gnss_time_timestamp.csv', index=False)
    temp_timestamp.to_csv('temperature_timestamp.csv', index=False)
    alt_pressure_timestamp.to_csv('altitude_pressure_timestamp.csv', index=False)
    humidity_timestamp.to_csv('humidity_timestamp.csv', index=False)
    gyro_timestamp.to_csv('gyro_spin_rate_timestamp.csv', index=False)
    voltage_timestamp.to_csv('voltage_timestamp.csv', index=False)

    time.sleep(1)