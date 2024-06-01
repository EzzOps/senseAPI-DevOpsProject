from flask import Flask, jsonify
import requests
from datetime import datetime, timedelta

app = Flask(__name__)

OPENSENSEMAP_API_URL = "https://api.opensensemap.org"

//  Example of endpoint to get senseBox data with temperature sensor
// "https://api.opensensemap.org/boxes?bbox=-180,-90,180,90&grouptags=temperature&format=json&full=true"

def get_version():
    response = requests.get(f"{OPENSENSEMAP_API_URL}/version")
    if response.status_code == 200:
        return response.json().get("version")
    else:
        return None

def get_temperature_data():
    response = requests.get(f"{OPENSENSEMAP_API_URL}/boxes?bbox=-180,-90,180,90&grouptags=temperature&format=json&full=true")
    if response.status_code == 200:
        return response.json()
    else:
        return None

def calculate_average_temperature(data):
    temperatures = []
    one_hour_ago = datetime.utcnow() - timedelta(hours=1)
    for box in data:
        for sensor in box['sensors']:
            if sensor['title'].lower() == 'temperature':
                for value in sensor['lastMeasurement']:
                    timestamp = datetime.strptime(value['createdAt'], '%Y-%m-%dT%H:%M:%S.%fZ')
                    if timestamp >= one_hour_ago:
                        temperatures.append(float(value['value']))
    if temperatures:
        return sum(temperatures) / len(temperatures)
    else:
        return None

@app.route('/version', methods=['GET'])
def version():
    version = get_version()
    if version:
        return jsonify({"version": version})
    else:
        return jsonify({"error": "Unable to fetch version"}), 500

@app.route('/temperature', methods=['GET'])
def temperature():
    data = get_temperature_data()
    if data:
        average_temp = calculate_average_temperature(data)
        if average_temp is not None:
            return jsonify({"average_temperature": average_temp})
        else:
            return jsonify({"error": "No recent temperature data found"}), 404
    else:
        return jsonify({"error": "Unable to fetch temperature data"}), 500

if __name__ == '__main__':
    app.run(debug=True)
