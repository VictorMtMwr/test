
from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Retrieve service URLs from environment variables
auth_service_url = os.getenv('AUTH_SERVICE_URL')
weather_service_url = os.getenv('WEATHER_SERVICE_URL')
recommendation_service_url = os.getenv('RECOMMENDATION_SERVICE_URL')

@app.route('/auth/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def auth_proxy(path):
    response = requests.request(
        method=request.method,
        url=f"{auth_service_url}/{path}",
        headers={key: value for (key, value) in request.headers},
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False)
    return (response.content, response.status_code, response.headers.items())

@app.route('/weather/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def weather_proxy(path):
    response = requests.request(
        method=request.method,
        url=f"{weather_service_url}/{path}",
        headers={key: value for (key, value) in request.headers},
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False)
    return (response.content, response.status_code, response.headers.items())

@app.route('/recommendations/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def recommendation_proxy(path):
    response = requests.request(
        method=request.method,
        url=f"{recommendation_service_url}/{path}",
        headers={key: value for (key, value) in request.headers},
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False)
    return (response.content, response.status_code, response.headers.items())

@app.route('/')
def index():
    return "Frontend API Gateway for WeatherWhisper Services"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
