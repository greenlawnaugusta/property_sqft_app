import requests
import json
import logging
import os
import cv2
import numpy as np
from IPython.display import Image, display

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set API keys
greenlawnaugusta_mapbox_token = os.getenv('MAPBOX_TOKEN')
google_maps_api_key = os.getenv('GOOGLE_MAPS_API_KEY')
gohighlevel_api_key = os.getenv('GOHIGHLEVEL_API_KEY')

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
