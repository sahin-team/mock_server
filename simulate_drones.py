import math
import requests
import time
import random
from datetime import datetime
import threading

BASE_URL = "http://localhost:5000"


def generate_dummy_data(team_num, init_lat, init_lon, prev_yaw, start_lat, start_lon, time_step, prev_altitude):
    # Constants
    R = 6378137  # Earth radius in meters
    MAX_DISTANCE = 250  # Maximum allowed distance from start in meters
    MAX_ALTITUDE = 100  # Maximum allowed altitude in meters
    MIN_ALTITUDE = 20   # Minimum allowed altitude in meters
    MAX_TURN_RATE = 10  # Maximum turn rate in degrees per second
    MAX_ALTITUDE_CHANGE_RATE = 2  # Maximum altitude change in meters per second
    
    def calculate_distance_and_bearing(lat1, lon1, lat2, lon2):
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        distance = 2 * R * math.asin(math.sqrt(a))
        bearing = math.atan2(math.sin(dlon) * math.cos(lat2),
                             math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(dlon))
        return distance, math.degrees(bearing)

    distance_from_start, bearing_to_start = calculate_distance_and_bearing(init_lat, init_lon, start_lat, start_lon)
    
    if distance_from_start > MAX_DISTANCE:
        # Gradually turn towards start point
        print(f"Team {team_num} is returning to the start point ========================================")
        target_direction = bearing_to_start
        speed = random.uniform(20, 30)  # Faster speed when returning
    else:
        # Continue in current direction with slight variations
        target_direction = prev_yaw
        speed = random.uniform(10, 20)

    # Calculate maximum allowed turn in this time step
    max_turn = MAX_TURN_RATE * time_step
    
    # Calculate the difference between current and target direction
    direction_diff = (target_direction - prev_yaw + 180) % 360 - 180
    
    # Limit the turn to the maximum allowed
    turn = max(min(direction_diff, max_turn), -max_turn)
    
    # Calculate new yaw
    new_yaw = (prev_yaw + turn) % 360

    # Use the new yaw for movement
    movement_direction = new_yaw

    # Calculate movement
    distance = speed * time_step
    delta_lat = distance / R * math.cos(math.radians(movement_direction))
    delta_lon = distance / (R * math.cos(math.radians(init_lat))) * math.sin(math.radians(movement_direction))

    new_lat = init_lat + math.degrees(delta_lat)
    new_lon = init_lon + math.degrees(delta_lon)

    # Update altitude with smoother transitions
    max_altitude_change = MAX_ALTITUDE_CHANGE_RATE * time_step
    altitude_change = random.uniform(-max_altitude_change, max_altitude_change)
    new_altitude = max(MIN_ALTITUDE, min(MAX_ALTITUDE, prev_altitude + altitude_change))

    # Update orientation
    new_pitch = random.uniform(-5, 5)  # Reduced pitch range for fixed-wing
    new_roll = random.uniform(-10, 10)  # Reduced roll range for fixed-wing

    # Simulate GPS inaccuracy
    gps_error = random.uniform(0, 5)  # GPS error up to 5 meters
    new_lat += random.uniform(-gps_error, gps_error) / R * (180 / math.pi)
    new_lon += random.uniform(-gps_error, gps_error) / (R * math.cos(math.pi * new_lat / 180)) * (180 / math.pi)

    return {
        "takim_numarasi": team_num,
        "iha_enlem": new_lat,
        "iha_boylam": new_lon,
        "iha_irtifa": new_altitude,
        "iha_dikilme": new_pitch,
        "iha_yonelme": new_yaw,
        "iha_yatis": new_roll,
        "iha_hizi": speed,
        "zaman_farki": int(time_step * 1000)  # Convert time step to milliseconds
    }



def send_telemetry(team_num, init_lat, init_lon, start_lat, start_lon):
    prev_yaw = 0
    prev_altitude = 50  # Starting altitude
    time_step = 1  # Time step in seconds

    while True:
        data = generate_dummy_data(team_num, init_lat, init_lon, prev_yaw, start_lat, start_lon, time_step, prev_altitude)
        prev_yaw = data["iha_yonelme"]
        prev_altitude = data["iha_irtifa"]
        try:
            response = requests.post(f"{BASE_URL}/api/telemetri_gonder", json=data)
            if response.status_code == 200:
                print(f"Team {team_num} sent telemetry data at {datetime.now()}")
                print("Response:", response.json())
                print("\n====================\n")
            else:
                print(f"Failed to send telemetry data for Team {team_num}. Status code:", response.status_code)
        except requests.exceptions.RequestException as e:
            print(f"Error sending telemetry data for Team {team_num}:", e)
        time.sleep(time_step)


def run_test():
    threads = []
    # Example initial positions around the stadium
    initial_positions = [
        (41.5, 36.1),
        (41.501, 36.101),
        (41.502, 36.102)
    ]
    start_positions = [
        (41.5, 36.1),
        (41.501, 36.101),
        (41.502, 36.102)
    ]
    
    for team_num, (init_lat, init_lon) in enumerate(initial_positions, start=1):
        start_lat, start_lon = start_positions[team_num-1]
        thread = threading.Thread(target=send_telemetry, args=(team_num, init_lat, init_lon, start_lat, start_lon), daemon=True)
        thread.start()
        threads.append(thread)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping test...")

if __name__ == "__main__":
    run_test()