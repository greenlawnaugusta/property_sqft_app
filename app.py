from flask import Flask, request, jsonify, redirect
from flask_cors import CORS
import logging
import os
import requests
import cv2
import numpy as np

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set API keys
greenlawnaugusta_mapbox_token = os.getenv('MAPBOX_TOKEN')
google_maps_api_key = os.getenv('GOOGLE_MAPS_API_KEY')
gohighlevel_api_key = os.getenv('GOHIGHLEVEL_API_KEY')

# Create the Flask app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# Function to get latitude and longitude using Google Maps API
def get_lat_lon(address):
    try:
        geocoding_endpoint = f'https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={google_maps_api_key}'
        response = requests.get(geocoding_endpoint)
        response.raise_for_status()
        geocode_data = response.json()
        if geocode_data['status'] == 'OK':
            location = geocode_data['results'][0]['geometry']['location']
            return location['lat'], location['lng']
        else:
            logging.warning(f"Geocoding failed for address {address}: {geocode_data['status']}")
            return None, None
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to fetch geocode data for address {address}: {e}")
        return None, None

# Define the API endpoint to receive address data
@app.route('/submit-address', methods=['POST'])
def submit_address():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        address = data.get('address')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        phone = data.get('phone')

        if not address or not first_name or not last_name or not email or not phone:
            return jsonify({'error': 'All fields are required'}), 400

        # Retrieve latitude and longitude for the address
        lat, lon = get_lat_lon(address)
        if lat is None or lon is None:
            return jsonify({'error': 'Failed to retrieve latitude and longitude'}), 500

        # For demonstration purposes, return success response
        # Normally, you'd continue with calculating turf area, pricing, etc.
        return jsonify({'success': 'Address processed successfully', 'contact_id': 'sample_contact_id'}), 200

    except Exception as e:
        logging.error(f"Error processing request: {str(e)}")
        return jsonify({'error': 'An error occurred while processing the request'}), 500

# Add CORS headers to all responses
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response

if __name__ == '__main__':
    # Run the Flask app
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
