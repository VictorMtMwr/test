from flask import Flask, jsonify, request
from weather_api import get_coordinates, get_weather
from flask_cors import CORS
import requests  # Para hacer la solicitud HTTP al recommendation-service

app = Flask(__name__)
CORS(app)

# Ruta para obtener los datos del clima y recomendaciones
@app.route('/recommendation', methods=['GET'])
def recommendation():
    city_name = request.args.get('city')
    if not city_name:
        return jsonify({"error": "El parámetro 'city' es obligatorio."}), 400
    
    location = get_coordinates(city_name)
    if location:
        weather_data = get_weather(f"{location[0]},{location[1]}")
        if weather_data:
            try:
                temperature = weather_data['data']['values']['temperature']
                
                # Llamar a la API del recommendation-service
                recommendation_response = requests.get(f'http://recommendation-service:5002/recommendation', params={'city': city_name})
                
                if recommendation_response.status_code == 200:
                    recommendation = recommendation_response.json().get('recommendation')
                else:
                    recommendation = "No se pudo obtener la recomendación."
                
                return jsonify({
                    "city": city_name,
                    "cordinates": location,
                    "temperature": temperature,
                    "recommendation": recommendation,
                })
            except KeyError as e:
                return jsonify({"error": f"Falta la clave: {str(e)}"}), 500
        return jsonify({"error": "No se pudo obtener los datos del clima"}), 500
    return jsonify({"error": "No se pudieron obtener las coordenadas"}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)
