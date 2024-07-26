from datetime import datetime, timedelta
import threading
import time
from flask import Flask, request, jsonify

app = Flask(__name__)

telemetry_data = {}
last_update_time = {}

session_info = {}
server_time = {
    "gun": 14,
    "saat": 11, 
    "dakika": 29,
    "saniye": 4,
    "milisaniye": 653
}

@app.route('/api/sunucusaati', methods=['GET'])
def get_server_time():
    return jsonify(server_time)

def update_server_time():
    global server_time
    while True:
        now = datetime.now()
        server_time = {
            "gun": now.day,
            "saat": now.hour,
            "dakika": now.minute,
            "saniye": now.second,
            "milisaniye": now.microsecond // 1000
        }
        time.sleep(0.1)

@app.route('/api/telemetri_gonder', methods=['POST'])
def send_telemetry():
    data = request.get_json()
    team_num = data.get('takim_numarasi')
    current_time = datetime.now()
    
    telemetry_data[team_num] = data
    last_update_time[team_num] = current_time
    
    two_seconds_ago = current_time - timedelta(seconds=2)

    
    response = {
        "sunucusaati": server_time,
        "konumBilgileri": [
            telemetry for t_num, telemetry in telemetry_data.items()
            if t_num != team_num and last_update_time.get(t_num, datetime.min) >= two_seconds_ago
        ]
    }
    
    
    return jsonify(response)


@app.route('/api/kilitlenme_bilgisi', methods=['POST'])
def send_lock_info():
    data = request.get_json()
    # Process the lock information
    return '', 200


@app.route('/api/kamikaze_bilgisi', methods=['POST'])
def send_kamikaze_info():
    data = request.get_json()
    # Process the kamikaze information
    return '', 200


@app.route('/api/qr_koordinati', methods=['GET'])
def get_qr_coordinates():
    qr_coordinates = {
        "x": 100,
        "y": 200
    }
    return jsonify(qr_coordinates)


@app.route('/api/hss_koordinatlari', methods=['GET'])
def get_hss_coordinates():
    hss_coordinates = {
        "lat": 41.1,
        "lon": 29.1
    }
    return jsonify(hss_coordinates)


@app.route('/api/redzones', methods=['GET'])
def get_redzones():
    current_time = datetime.now()
    response = {
        "sunucusaati": {
            "gun": current_time.day,
            "saat": current_time.hour,
            "dakika": current_time.minute,
            "saniye": current_time.second,
            "milisaniye": current_time.microsecond // 1000
        },
        "hss_koordinat_bilgileri": [
            {
                "id": 0,
                "hssEnlem": 40.23260922,
                "hssBoylam": 29.00573015,
                "hssYaricap": 50
            },
            {
                "id": 1,
                "hssEnlem": 40.23351019,
                "hssBoylam": 28.99976492,
                "hssYaricap": 50
            },
            {
                "id": 2,
                "hssEnlem": 40.23105297,
                "hssBoylam": 29.00744677,
                "hssYaricap": 75
            },
            {
                "id": 3,
                "hssEnlem": 40.23090554,
                "hssBoylam": 29.00221109,
                "hssYaricap": 150
            }
        ]
    }
    return jsonify(response)


if __name__ == '__main__':
    threading.Thread(target=update_server_time, daemon=True).start()
    app.run(debug=True)