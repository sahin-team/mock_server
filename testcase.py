import requests
import time
import random
from datetime import datetime
import threading

BASE_URL = "http://localhost:5000"

def generate_dummy_data(team_num):
    return {
        "takim_numarasi": team_num,
        "iha_enlem": 41.5 + random.uniform(-0.01, 0.01),
        "iha_boylam": 36.1 + random.uniform(-0.01, 0.01),
        "iha_irtifa": random.uniform(30, 50),
        "iha_dikilme": random.uniform(-10, 10),
        "iha_yonelme": random.uniform(0, 359),
        "iha_yatis": random.uniform(-45, 45),
        "iha_hizi": random.uniform(35, 50),
        "zaman_farki": random.randint(0, 500)
    }

def send_telemetry(team_num):
    while True:
        data = generate_dummy_data(team_num)
        try:
            response = requests.post(f"{BASE_URL}/api/telemetri_gonder", json=data)
            if response.status_code == 200:
                print(f"Team {team_num} sent telemetry data at {datetime.now()}")
                print("Response:", response.json())
            else:
                print(f"Failed to send telemetry data for Team {team_num}. Status code:", response.status_code)
        except requests.exceptions.RequestException as e:
            print(f"Error sending telemetry data for Team {team_num}:", e)
        time.sleep(1)

def run_test():
    threads = []
    for team_num in range(1, 4):
        thread = threading.Thread(target=send_telemetry, args=(team_num,), daemon=True)
        thread.start()
        threads.append(thread)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping test...")

if __name__ == "__main__":
    run_test()