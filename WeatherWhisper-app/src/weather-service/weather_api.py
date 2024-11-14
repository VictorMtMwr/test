from flask import Flask, jsonify, request
from weather_api import get_coordinates, get_weather
from flask_cors import CORS
import requests  # Para hacer la solicitud HTTP al recommendation-service

app = Flask(__name__)
CORS(app)
import requests

API_KEY_TOMORROW = "gcRChK23DGmoCYen6tVm3XX73Jxfuwh9"
API_KEY_OPENCAGE = "8795cc1289d9432297a2a878903f3891"

def get_coordinates(city_name):
    url = f"https://api.opencagedata.com/geocode/v1/json?q={city_name}&key={API_KEY_OPENCAGE}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            coordinates = data['results'][0]['geometry']
            return (coordinates['lat'], coordinates['lng'])
    return None

def get_weather(location):
    url = f"https://api.tomorrow.io/v4/weather/realtime?location={location}&apikey={API_KEY_TOMORROW}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

@app.route('/weather', methods=['GET'])
def weather_info():
    city_name = request.args.get('city')
    location = get_coordinates(city_name)
    if location:
        weather_data = get_weather(f"{location[0]},{location[1]}")
        return jsonify(weather_data)
    return jsonify({"error": "No se encontraron datos del clima"}), 404

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)