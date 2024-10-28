from flask import Flask, request, jsonify, redirect 
import requests
import json
import logging
import cv2
import numpy as np
from flask_cors import CORS
import os

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Set API keys
greenlawnaugusta_mapbox_token = 'sk.eyJ1IjoiZ3JlZW5sYXduYXVndXN0YSIsImEiOiJjbTJrNWhqYXQwZDVlMmpwdzd4bDl0bGdqIn0.DFYXkt-2thT24YRg9tEdWg'
google_maps_api_key = 'AIzaSyBOLtey3T6ug8ZBfvZl-Mu2V9kJpRtcQeo'
gohighlevel_api_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJsb2NhdGlvbl9pZCI6InZKTk5QbW5tT3dGbzZvRFROQ0FNIiwiY29tcGFueV9pZCI6IlZGU0lKQWpDNEdQZzhLY2FuZlJuIiwidmVyc2lvbiI6MSwiaWF0IjoxNzAwNDEyNTU2OTc2LCJzdWIiOiJ1c2VyX2lkIn0.13KR3p9bWk-ImURthHgHZSJIk44MVnOMG8WjamUVf3Y'

# Create the Flask app
app = Flask(__name__)
CORS(app, resources={r"/.*": {"origins": ["https://api.leadconnectorhq.com", "*"]}}, supports_credentials=True)

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
            error_message = geocode_data.get('error_message', 'No detailed error message provided')
            logging.warning(f"Geocoding failed for address {address}: {geocode_data['status']} - {error_message}")
            return None, None
    else:
        logging.error(f"Failed to fetch geocode data for address {address}: {response.status_code} - {response.text}")
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
        "recurring_maintenance_price": str(price),
        "one_time_mow_price": str(price * 1.15),
        "weed_control_1_price": str(price * 0.8),
        "weed_control_2_price": str(price * 0.9),
        "turf_sq_ft": str(turf_sq_ft)
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
        "latitude": str(lat),
        "longitude": str(lon),
        "customField": {
            "Recurring Maintenance Price": pricing_info["recurring_maintenance_price"],
            "One Time Mow Price": pricing_info["one_time_mow_price"],
            "Weed Control 1 Price": pricing_info["weed_control_1_price"],
            "Weed Control 2 Price": pricing_info["weed_control_2_price"],
            "Turf Sq Ft": pricing_info["turf_sq_ft"]
        }
    }

    # Debugging: Log the contact data payload
    logging.debug(f"Sending contact data to GoHighLevel: {json.dumps(contact_data, indent=2)}")

    response = requests.post(url, headers=headers, json=contact_data)
    
    # Log response details for debugging
    logging.debug(f"Response status code: {response.status_code}")
    logging.debug(f"Response headers: {response.headers}")
    logging.debug(f"Response text: {response.text}")

    if response.status_code in [200, 201]:
        logging.info("Successfully created or updated contact in GoHighLevel with pricing information.")
        return response.json().get("contact", {}).get("id")
    else:
        logging.error(f"Failed to create or update contact in GoHighLevel: {response.status_code} - {response.text}")
       
