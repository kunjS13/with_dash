import math

#Velocity Calculation

def calculate_velocity(gps_lat, gps_lon, gps_alt):
    # Convert latitude and longitude to radians
    lat_rad = math.radians(gps_lat)
    lon_rad = math.radians(gps_lon)

    # Earth's radius in meters
    earth_radius = 6371000

    # Calculate x, y, and z velocity components
    x_velocity = gps_alt * math.cos(lat_rad) * math.cos(lon_rad)
    y_velocity = gps_alt * math.cos(lat_rad) * math.sin(lon_rad)
    z_velocity = gps_alt * math.sin(lat_rad)

    return x_velocity, y_velocity, z_velocity

# Example usage
gps_lat = 37.7749
gps_lon = -122.4194
gps_alt = 100

x_vel, y_vel, z_vel = calculate_velocity(gps_lat, gps_lon, gps_alt)
print(f"X Velocity: {x_vel} m/s")
print(f"Y Velocity: {y_vel} m/s")
print(f"Z Velocity: {z_vel} m/s")
