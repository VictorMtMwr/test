import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# URL del servicio weather-service 
WEATHER_SERVICE_URL = 'http://weather-service:5001/weather'

@app.route('/recommendation', methods=['GET'])
def recommendation():
    city_name = request.args.get('city')
    if not city_name:
        return jsonify({"error": "El parámetro 'city' es obligatorio."}), 400

    # Hacer una solicitud al weather-service para obtener los datos climáticos
    weather_response = requests.get(f"{WEATHER_SERVICE_URL}?city={city_name}")
    
    if weather_response.status_code == 200:
        weather_data = weather_response.json()
        
        temperature = weather_data['temperature']
        humidity = weather_data['humidity']
        uv_index = weather_data['uv_index']
        
        # Crear la recomendación de vestimenta basada en la temperatura
        recommendation = get_clothing_recommendation(temperature)
        
        return jsonify({
            "city": city_name,
            "temperature": temperature,
            "humidity": humidity,
            "uv_index": uv_index,
            "recommendation": recommendation
        })
    else:
        return jsonify({"error": "No se pudo obtener los datos del clima"}), 500

def get_clothing_recommendation(temperature):
    if temperature < 0:
        return "Usa un abrigo pesado, guantes y una bufanda."
    elif 0 <= temperature < 15:
        return "Usa una chaqueta cálida, pantalones largos y un suéter."
    elif 15 <= temperature < 25:
        return "Una chaqueta ligera o suéter y pantalones largos son adecuados."
    else:
        return "Vístete con una camiseta ligera y shorts."

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002)
