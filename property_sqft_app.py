from flask import Flask, request, jsonify, redirect
import requests
import json
import logging
import cv2
import numpy as np
from flask_cors import CORS
import os

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set API keys
greenlawnaugusta_mapbox_token = os.getenv('MAPBOX_TOKEN')
google_maps_api_key = os.getenv('GOOGLE_MAPS_API_KEY')
gohighlevel_api_key = os.getenv('GOHIGHLEVEL_API_KEY')

# Create the Flask app
app = Flask(__name__)
CORS(app)

# Function to get latitude and longitude using Google Maps API
def get_lat_lon(address):
    geocoding_endpoint = f'https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={google_maps_api_key}'
    response = requests.get(geocoding_endpoint)
    if response.status_code == 200:
        geocode_data = response.json()
        if geocode_data['status'] == 'OK':
            location = geocode_data['results'][0]['geometry']['location']
            return location['lat'], location['lng']
        else:
            logging.warning(f"Geocoding failed for address {address}: {geocode_data['status']}")
            return None, None
    else:
        logging.error(f"Failed to fetch geocode data for address {address}: {response.status_code}")
        return None, None

# Function to calculate turf area using placeholder implementation
def calculate_turf_area(lat, lon):
    # Placeholder logic to calculate the turf area
    return 5000  # Replace with your actual logic

# Function to calculate pricing based on turf area
def calculate_pricing(turf_sq_ft):
    # Calculate price based on turf square footage
    if turf_sq_ft <= 4000:
        price = 50
    else:
        price = 50 + np.ceil((turf_sq_ft - 4000) / 100) * 1.3
    
    pricing_info = {
        "recurring_maintenance_price": price,
        "one_time_mow_price": price * 1.15
    }
    return pricing_info

# Function to create or update a contact in GoHighLevel
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
            "one_time_mow_price": pricing_info["one_time_mow_price"]
        }
    }

    response = requests.post(url, headers=headers, json=contact_data)
    if response.status_code in [200, 201]:
        logging.info("Successfully created or updated contact in GoHighLevel with pricing information.")
        return response.json().get("contact", {}).get("id")
    else:
        logging.error(f"Failed to create or update contact in GoHighLevel: {response.status_code} - {response.text}")
        return None

# Define an API endpoint to receive address data
@app.route('/submit-address', methods=['POST'])
def submit_address():
    try:
        # Get JSON data from request
        data = request.get_json()
        address = data.get('address')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        phone = data.get('phone')

        if not all([address, first_name, last_name, email, phone]):
            return jsonify({'error': 'All fields are required'}), 400

        # Get latitude and longitude
        lat, lon = get_lat_lon(address)
        if lat is None or lon is None:
            return jsonify({'error': 'Failed to retrieve latitude and longitude'}), 500

        # Calculate turf area and pricing
        turf_sq_ft = calculate_turf_area(lat, lon)
        pricing_info = calculate_pricing(turf_sq_ft)

        # Create or update the contact in GoHighLevel
        contact_id = create_or_update_gohighlevel_contact(first_name, last_name, email, phone, address, lat, lon, pricing_info)
        if not contact_id:
            return jsonify({'error': 'Failed to create or update contact'}), 500

        # Redirect to funnel page with pricing information
        redirect_url = f"https://pricing.greenlawnaugusta.com/pricing-page?contact_id={contact_id}&price={pricing_info['recurring_maintenance_price']}"
        return redirect(redirect_url)

    except Exception as e:
        logging.error(f"Error processing request: {str(e)}")
        return jsonify({'error': 'An error occurred while processing the request'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
