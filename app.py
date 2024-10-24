from flask import Flask, request, jsonify
import logging
import os
import requests
import cv2
import numpy as np

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set Mapbox tokens
greenlawnaugusta_mapbox_token = 'sk.eyJ1IjoiZ3JlZW5sYXduYXVndXN0YSIsImEiOiJjbTJrNWhqYXQwZDVlMmpwdzd4bDl0bGdqIn0.DFYXkt-2thT24YRg9tEdWg'

# Create the Flask app
app = Flask(__name__)

# Function to get latitude and longitude using Google Maps API
def get_lat_lon(address):
    google_maps_api_key = 'AIzaSyBOLtey3T6ug8ZBfvZl-Mu2V9kJpRtcQeo'
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
        price = 50 + np.ceil((turf_sq_ft - 4000) / 100) * 1.1

    # Adjust price based on service type
    recurring_maintenance_price = price
    one_time_mow_price = recurring_maintenance_price * 1.15
    full_service_price = recurring_maintenance_price * 1.25

    # Calculate weed control prices
    if turf_sq_ft <= 4000:
        weed_control_price = 50
    else:
        weed_control_price = 50 + np.ceil((turf_sq_ft - 4000) / 100) * 1.1

    weed_control_1_price = weed_control_price
    weed_control_2_price = weed_control_1_price * 1.10
    weed_control_3_price = weed_control_1_price * 1.15

    pricing_info = {
        "recurring_maintenance_price": recurring_maintenance_price,
        "one_time_mow_price": one_time_mow_price,
        "full_service_price": full_service_price,
        "weed_control_1_price": weed_control_1_price,
        "weed_control_2_price": weed_control_2_price,
        "weed_control_3_price": weed_control_3_price
    }

    return pricing_info

# Define an API endpoint to receive address data
@app.route('/submit-address', methods=['POST'])
def submit_address():
    try:
        # Get JSON data from request
        data = request.get_json()
        address = data.get('address')

        if not address:
            return jsonify({'error': 'Address is required'}), 400

        # Get latitude and longitude
        lat, lon = get_lat_lon(address)
        if lat is None or lon is None:
            return jsonify({'error': 'Failed to retrieve latitude and longitude'}), 500

        # Calculate turf area
        turf_sq_ft = calculate_turf_area(lat, lon)
        if isinstance(turf_sq_ft, str):
            return jsonify({'error': turf_sq_ft}), 500

        # Calculate pricing
        pricing_info = calculate_pricing(turf_sq_ft)

        response = {
            'turf_area_sq_ft': turf_sq_ft,
            'pricing': pricing_info
        }

        return jsonify(response), 200

    except Exception as e:
        logging.error(f"Error processing request: {str(e)}")
        return jsonify({'error': 'An error occurred while processing the request'}), 500

if __name__ == '__main__':
    # Run the Flask app
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
