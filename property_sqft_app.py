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

# Function to calculate pricing based on turf area (for simplicity)
def calculate_pricing(turf_sq_ft):
    price = 50 if turf_sq_ft <= 4000 else 50 + (turf_sq_ft - 4000) * 0.03
    return {
        "recurring_maintenance_price": price,
        "one_time_mow_price": price * 1.1,
        "full_service_price": price * 1.25
    }

# Function to create or update a contact in GoHighLevel with pricing data
def create_or_update_gohighlevel_contact(first_name, last_name, email, phone, address, lat, lon, pricing_info):
    url = "https://rest.gohighlevel.com/v1/contacts/"
    headers = {
        "Authorization": f"Bearer {gohighlevel_api_key}",
        "Content-Type": "application/json"
    }
    contact_data = {
        "firstName": first_name,
        "lastName": last_name,
        "email": email,
        "phone": phone,
        "address1": address,
        "latitude": lat,
        "longitude": lon,
        "customField": {
            "recurring_maintenance_price": pricing_info["recurring_maintenance_price"],
            "one_time_mow_price": pricing_info["one_time_mow_price"],
            "full_service_price": pricing_info["full_service_price"]
        }
    }

    response = requests.post(url, headers=headers, json=contact_data)
    if response.status_code in [200, 201]:
        contact = response.json()
        logging.info("Successfully created or updated contact in GoHighLevel with pricing information.")
        return contact["contact"]["id"]
    else:
        logging.error(f"Failed to create or update contact in GoHighLevel: {response.status_code} - {response.text}")
        return None

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

        # Calculate turf area and pricing
        turf_sq_ft = 4000  # Placeholder for turf calculation
        pricing_info = calculate_pricing(turf_sq_ft)

        # Create or update GoHighLevel contact
        contact_id = create_or_update_gohighlevel_contact(first_name, last_name, email, phone, address, lat, lon, pricing_info)
        if not contact_id:
            return jsonify({'error': 'Failed to create or update contact in GoHighLevel'}), 500

        # Redirect the user to the pricing funnel page with parameters
        redirect_url = f"https://pricing.greenlawnaugusta.com/pricing-page?contact_id={contact_id}&turf_sq_ft={turf_sq_ft}&recurring_price={pricing_info['recurring_maintenance_price']}&one_time_price={pricing_info['one_time_mow_price']}&full_service_price={pricing_info['full_service_price']}"
        return jsonify({'redirect_url': redirect_url}), 200

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
