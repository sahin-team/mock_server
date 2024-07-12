from flask import Flask, request, jsonify

app = Flask(__name__)


teamUsername = "sahin"
teamPassword = "sahin1234"
# Dummy data for testing
telemetry_data = {
    1: {
        "takim_numarasi": 1,
        "iha_enlem": 41.5118256,
        "iha_boylam": 36.11993,
        "iha_irtifa": 36.0,
        "iha_dikilme": -8.0,
        "iha_yonelme": 127,
        "iha_yatis": 19.0,
        "iha_hizi": 41.0,
        "zaman_farki": 467
    },
    2: {
        "takim_numarasi": 2,
        "iha_enlem": 41.5100365,
        "iha_boylam": 36.11837,
        "iha_irtifa": 44.0,
        "iha_dikilme": 24.0,
        "iha_yonelme": 277.0,
        "iha_yatis": -37.0,
        "iha_hizi": 40.0,
        "zaman_farki": 248
    },
    3: {
        "takim_numarasi": 3,
        "iha_enlem": 41.5123138,
        "iha_boylam": 36.12,
        "iha_irtifa": 32.0,
        "iha_dikilme": 9.0,
        "iha_yonelme": 13,
        "iha_yatis": -30.0,
        "iha_hizi": 45.0,
        "zaman_farki": 30
    }
}

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


@app.route('/api/telemetri_gonder', methods=['POST'])
def send_telemetry():
    data = request.get_json()
    team_num = data.get('takim_numarasi')
    # telemetry_data[team_num] = data
    
    response = {
        "sunucusaati": server_time,
        "konumBilgileri": list(telemetry_data.values())
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

from flask import Flask, jsonify
from datetime import datetime

app = Flask(__name__)

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

@app.route('/api/giris', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('kadi')
    password = data.get('sifre')
    if username == teamUsername and password == teamPassword:
        session_info[username] = "some_session_token"
        return jsonify({"status": "success"}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 400


if __name__ == '__main__':
    app.run(debug=True)
