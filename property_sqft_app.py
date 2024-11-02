import os
import json
import requests
import logging
import cv2
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set API keys from environment variables
greenlawnaugusta_mapbox_token = os.getenv('GREENLAWNAUGUSTA_MAPBOX_TOKEN', 'sk.eyJ1IjoiZ3JlZW5sYXduYXVndXN0YSIsImEiOiJjbTJrNWhqYXQwZDVlMmpwdzd4bDl0bGdqIn0.DFYXkt-2thT24YRg9tEdWg')
google_maps_api_key = os.getenv('GOOGLE_MAPS_API_KEY', 'AIzaSyBOLtey3T6ug8ZBfvZl-Mu2V9kJpRtcQeo')
gohighlevel_api_key = os.getenv('GOHIGHLEVEL_API_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJsb2NhdGlvbl9pZCI6InZKTk5QbW5tT3dGbzZvRFROQ0FNIiwiY29tcGFueV9pZCI6IlZGU0lKQWpDNEdQZzhLY2FuZlJuIiwidmVyc2lvbiI6MSwiaWF0IjoxNzAwNDEyNTU2OTc2LCJzdWIiOiJ1c2VyX2lkIn0.13KR3p9bWk-ImURthHgHZSJIk44MVnOMG8WjamUVf3Y')

# Create Flask app
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

# Function to calculate turf area using OpenCV and Mapbox Satellite Imagery
def calculate_turf_area(lat, lon):
    try:
        # Fetch satellite image from Mapbox Static API
        mapbox_url = f"https://api.mapbox.com/styles/v1/mapbox/satellite-v9/static/{lon},{lat},20/1000x1000?access_token={greenlawnaugusta_mapbox_token}"
        response = requests.get(mapbox_url)
        response.raise_for_status()
        image_path = 'satellite_image.png'
        with open(image_path, 'wb') as f:
            f.write(response.content)

        # Load the satellite image
        image = cv2.imread(image_path)
        if image is None:
            logging.error("Failed to load satellite image.")
            return "Failed to load satellite image."

        # Convert the image to HSV color space for better segmentation
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # Define color range for dormant turf (beige/tan grass)
        lower_beige = np.array([10, 0, 80])
        upper_beige = np.array([30, 100, 255])

        # Create a mask for beige/tan areas
        mask = cv2.inRange(hsv_image, lower_beige, upper_beige)

        # Perform morphological operations to reduce noise
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

        # Calculate the area of the beige/tan regions
        turf_area = cv2.countNonZero(mask)

        # Adjust pixel_area based on known lot size
        known_lot_size = 9915  # Lot size from manual measurement in square feet
        total_pixels = mask.shape[0] * mask.shape[1]
        pixel_area = known_lot_size / total_pixels  # Calibrate pixel area based on lot size

        # Introduce a correction factor to improve accuracy
        correction_factor = 2.5  # Adjusted factor based on further testing and calibration
        turf_sq_ft = turf_area * pixel_area * correction_factor

        logging.info(f"Calculated turf area: {turf_sq_ft} sq ft")

        # Clean up image file after processing
        os.remove(image_path)

        return turf_sq_ft

    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching satellite image from Mapbox: {str(e)}")
        return f"Error fetching satellite image from Mapbox: {str(e)}"

# Function to calculate pricing based on turf area
def calculate_pricing(turf_sq_ft):
    # Calculate price based on turf square footage
    if turf_sq_ft <= 4000:
        price = 50
    else:
        price = 50 + np.ceil((turf_sq_ft - 4000) / 100) * 1.3

    # Adjust price based on service type
    recurring_maintenance_biweekly_price = price
    recurring_maintenance_weekly_price = recurring_maintenance_biweekly_price * 0.75
    one_time_mow_price = recurring_maintenance_biweekly_price * 1.15
    full_service_biweekly_price = recurring_maintenance_biweekly_price * 1.25
    full_service_weekly_price = full_service_biweekly_price * 0.90

    # Calculate weed control prices
    if turf_sq_ft <= 4000:
        weed_control_price = 50
    else:
        weed_control_price = 50 + np.ceil((turf_sq_ft - 4000) / 100) * 1.3

    weed_control_1_price = weed_control_price
    weed_control_2_price = weed_control_1_price * 1.10
    weed_control_3_price = weed_control_1_price * 1.15

    pricing_info = {
        "recurring_maintenance_weekly_price": recurring_maintenance_weekly_price,
        "recurring_maintenance_biweekly_price": recurring_maintenance_biweekly_price,
        "one_time_mow_price": one_time_mow_price,
        "full_service_weekly_price": full_service_weekly_price,
        "full_service_biweekly_price": full_service_biweekly_price,
        "weed_control_1_price": weed_control_1_price,
        "weed_control_2_price": weed_control_2_price,
        "weed_control_3_price": weed_control_3_price,
        "turf_sq_ft": turf_sq_ft
    }

    logging.info(f"Calculated pricing: {json.dumps(pricing_info, indent=4)}")
    return pricing_info

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
        "customFields": [  # Corrected from customField to customFields (list format)
            {"name": "weed_control_1_price", "value": pricing_info["weed_control_1_price"]},
            {"name": "weed_control_2_price", "value": pricing_info["weed_control_2_price"]},
            {"name": "weed_control_3_price", "value": pricing_info["weed_control_3_price"]},
            {"name": "recurring_maintenance_price", "value": pricing_info["recurring_maintenance_biweekly_price"]},
            {"name": "one_time_mow_price", "value": pricing_info["one_time_mow_price"]},
            {"name": "full_service_price", "value": pricing_info["full_service_biweekly_price"]},
            {"name": "turf_sq_ft", "value": pricing_info["turf_sq_ft"]}
        ]
    }

    response = requests.post(url, headers=headers, json=contact_data)
    if response.status_code in [200, 201]:
        contact = response.json()
        logging.info("Successfully created or updated contact in GoHighLevel with pricing information.")
        return contact.get("contact", {}).get("id")
    else:
        logging.error(f"Failed to create or update contact in GoHighLevel: {response.status_code} - {response.text}")
        return None

# Flask route to handle turf area and pricing calculation
@app.route('/calculate', methods=['POST'])
def calculate():
    if request.content_type == 'application/json':
        data = request.json
    else:
        data = request.form

    address = data.get('address')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')
    phone = data.get('phone')

    lat, lon = get_lat_lon(address)
    if lat is not None and lon is not None:
        turf_sq_ft = calculate_turf_area(lat, lon)
        if isinstance(turf_sq_ft, str):
            return jsonify({"error": turf_sq_ft}), 400
        else:
            pricing_info = calculate_pricing(turf_sq_ft)
            contact_id = create_or_update_gohighlevel_contact(first_name, last_name, email, phone, address, lat, lon, pricing_info)
            return jsonify({
                "turf_sq_ft": turf_sq_ft,
                "pricing_info": pricing_info,
                "contact_id": contact_id,
                "redirect_url": f"https://pricing.greenlawnaugusta.com/pricing-page?contact_id={contact_id}"
            })
    else:
        return jsonify({"error": "Failed to retrieve latitude and longitude for the address."}), 400

# Flask route to retrieve contact data (proxy)
@app.route('/proxy/gohighlevel/<contact_id>', methods=['GET'])
def proxy_gohighlevel(contact_id):
    url = f"https://rest.gohighlevel.com/v1/contacts/{contact_id}"
    headers = {
        "Authorization": f"Bearer {gohighlevel_api_key}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        contact_data = response.json()
        if "contact" in contact_data:
            return jsonify(contact_data), response.status_code
        else:
            return jsonify({"error": "Contact data is missing"}), 404
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500

# Start Flask app
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
