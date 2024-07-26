import random
import time
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from havers import haversine_distance
from testcase import generate_dummy_data

def print_telemetry_data(data):
    print("Telemetry Data:")
    print(f"  Team Number: {data['takim_numarasi']}")
    print(f"  Latitude: {data['iha_enlem']:.8f}")
    print(f"  Longitude: {data['iha_boylam']:.8f}")
    print(f"  Altitude: {data['iha_irtifa']:.2f} meters")
    print(f"  Pitch: {data['iha_dikilme']:.2f} degrees")
    print(f"  Yaw: {data['iha_yonelme']:.2f} degrees")
    print(f"  Roll: {data['iha_yatis']:.2f} degrees")
    print(f"  Speed: {data['iha_hizi']:.2f} m/s")
    print(f"  Time Difference: {data['zaman_farki']} milliseconds")
    print(f"  Timestamp: {datetime.now()}")
    print()

def plot_path(latitudes, longitudes, start_lat, start_lon):
    plt.figure(figsize=(12, 8))
    plt.plot(longitudes, latitudes, marker='.', linestyle='-', color='b', markersize=2)
    plt.plot(start_lon, start_lat, marker='o', color='r', markersize=10, label='Start Point')
    plt.plot(longitudes[-1], latitudes[-1], marker='s', color='g', markersize=8, label='End Point')
    plt.title('Drone Path Over Simulation Period')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_altitude(altitudes, timestamps):
    plt.figure(figsize=(12, 6))
    plt.plot(timestamps, altitudes, linestyle='-', color='b')
    plt.title('Drone Altitude Over Time')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Altitude (meters)')
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    team_num = 1
    start_lat = 41.1016030590917
    start_lon = 29.02335114170372
    init_lat = start_lat
    init_lon = start_lon
    init_yaw = random.uniform(0, 359)
    init_altitude = 30  # Starting altitude

    latitudes = [init_lat]
    longitudes = [init_lon]
    altitudes = [init_altitude]
    timestamps = [0]
    prev_yaw = init_yaw
    prev_altitude = init_altitude
    simulation_time = 1200  # 20 minutes in seconds
    time_step = 1  # 1 second intervals
    
    max_distance = 0

    for t in range(0, simulation_time, time_step):
        data = generate_dummy_data(team_num, latitudes[-1], longitudes[-1], prev_yaw, start_lat, start_lon, time_step, prev_altitude)
        print_telemetry_data(data)
        
        latitudes.append(data['iha_enlem'])
        longitudes.append(data['iha_boylam'])
        altitudes.append(data['iha_irtifa'])
        timestamps.append(t + time_step)
        
        prev_yaw = data['iha_yonelme']
        prev_altitude = data['iha_irtifa']
        
        current_distance = haversine_distance(start_lat, start_lon, data['iha_enlem'], data['iha_boylam'])
        max_distance = max(max_distance, current_distance)
        
        # Uncomment the line below if you want to see the simulation in real-time
        # time.sleep(time_step)
    print(f"Maximum distance from start point: {max_distance:.2f} meters")
    # Plot the path after simulation
    plot_path(latitudes, longitudes, start_lat, start_lon)
    
    # Plot altitude over time
    plot_altitude(altitudes, timestamps)