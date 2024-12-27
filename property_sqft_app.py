from flask import Flask, request, jsonify
import requests
import logging
import os
import cv2
import numpy as np
import stripe
from flask_cors import CORS

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set API keys
greenlawnaugusta_mapbox_token = 'sk.eyJ1IjoiZ3JlZW5sYXduYXVndXN0YSIsImEiOiJjbTJrNWhqYXQwZDVlMmpwdzd4bDl0bGdqIn0.DFYXkt-2thT24YRg9tEdWg'
google_maps_api_key = 'AIzaSyBOLtey3T6ug8ZBfvZl-Mu2V9kJpRtcQeo'
gohighlevel_api_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJsb2NhdGlvbl9pZCI6InZKTk5QbW5tT3dGbzZvRFROQ0FNIiwiY29tcGFueV9pZCI6IlZGU0lKQWpDNEdQZzhLY2FuZlJuIiwidmVyc2lvbiI6MSwiaWF0IjoxNzAwNDEyNTU2OTc2LCJzdWIiOiJ1c2VyX2lkIn0.13KR3p9bWk-ImURthHgHZSJIk44MVnOMG8WjamUVf3Y'
STRIPE_PUBLIC_KEY = 'pk_live_51OPSgJBjzAiuXy5VmNJUKcpgpLvACac5RJf08tOX1xdMFF1dX09jAAcwNP6rIb50XJPWcmzhk1EApRgdhOHVXb1p00jbSoFD8Y'
STRIPE_SECRET_KEY = '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'

stripe.api_key = STRIPE_SECRET_KEY

# Create Flask app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["https://pricing.greenlawnaugusta.com/home-page"]}}, supports_credentials=True)

@app.route('/create-products', methods=['POST', 'OPTIONS'])
def create_products():
    """Handle product creation in Stripe."""
    if request.method == 'OPTIONS':
        response = jsonify({'message': 'CORS preflight handled'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        response.status_code = 200
        return response

    try:
        data = request.json
        pricing_info = data.get('pricing_info')

        if not pricing_info:
            return jsonify({"error": "Missing pricing info."}), 400

        products = []
        for service_name, price in pricing_info.items():
            if service_name != "turf_sq_ft":
                product = stripe.Product.create(name=service_name)
                price_data = stripe.Price.create(
                    unit_amount=int(price * 100),  # Stripe expects the price in cents
                    currency="usd",
                    product=product.id
                )
                products.append({"name": service_name, "price_id": price_data.id})

        return jsonify({"products": products}), 200
    except Exception as e:
        logging.error(f"Error in create-products: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Function to calculate pricing
def calculate_pricing(turf_sq_ft):
    base_price = 50 if turf_sq_ft <= 4000 else 50 + np.ceil((turf_sq_ft - 4000) / 100) * 1.3
    return {
        "recurring_maintenance_biweekly_price": base_price,
        "recurring_maintenance_weekly_price": base_price * 0.75,
        "one_time_mow_price": base_price * 1.15,
        "full_service_biweekly_price": base_price * 1.25,
        "full_service_weekly_price": base_price * 1.25 * 0.90,
        "weed_control_1_price": base_price * 1.1,
        "weed_control_2_price": base_price * 1.15,
        "weed_control_3_price": base_price * 1.2,
        "turf_sq_ft": turf_sq_ft,
    }

# Pricing Calculation Endpoint
@app.route('/calculate-prices', methods=['POST', 'OPTIONS'])
def calculate_prices():
    if request.method == 'OPTIONS':
        response = jsonify({'message': 'CORS preflight handled'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        response.status_code = 200
        return response

    try:
        data = request.json
        turf_sq_ft = data.get('turf_sq_ft')

        if not turf_sq_ft:
            return jsonify({"error": "Turf square footage is required."}), 400

        pricing_info = calculate_pricing(turf_sq_ft)
        services = [
            {"name": service_name, "price": price, "price_id": f"mock_price_{service_name}"}
            for service_name, price in pricing_info.items() if service_name != "turf_sq_ft"
        ]

        return jsonify({"services": services}), 200
    except Exception as e:
        logging.error(f"Error in calculate-prices: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Function to get latitude and longitude using Google Maps API
def get_lat_lon(address):
    try:
        geocoding_endpoint = f'https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={google_maps_api_key}'
        response = requests.get(geocoding_endpoint)
        if response.status_code == 200:
            geocode_data = response.json()
            if geocode_data['status'] == 'OK':
                location = geocode_data['results'][0]['geometry']['location']
                return location['lat'], location['lng']
            else:
                logging.warning(f"Geocoding failed for address: {address}. Error: {geocode_data.get('error_message', geocode_data['status'])}")
        else:
            logging.error(f"HTTP error fetching geocode data. Status code: {response.status_code}")
    except Exception as e:
        logging.error(f"Exception during geocoding: {str(e)}")
    return None, None

# Function to calculate turf area using Mapbox satellite imagery
def calculate_turf_area(lat, lon):
    try:
        mapbox_url = f"https://api.mapbox.com/styles/v1/mapbox/satellite-v9/static/{lon},{lat},20/1000x1000?access_token={greenlawnaugusta_mapbox_token}"
        response = requests.get(mapbox_url)
        response.raise_for_status()
        image_path = 'satellite_image.png'
        with open(image_path, 'wb') as f:
            f.write(response.content)

        image = cv2.imread(image_path)
        if image is None:
            logging.error("Failed to load satellite image.")
            return "Failed to load satellite image."

        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        lower_beige = np.array([10, 0, 80])
        upper_beige = np.array([30, 100, 255])
        mask = cv2.inRange(hsv_image, lower_beige, upper_beige)

        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

        turf_area = cv2.countNonZero(mask)
        known_lot_size = 9915  # Example value, update based on actual lot size
        total_pixels = mask.shape[0] * mask.shape[1]
        pixel_area = known_lot_size / total_pixels
        correction_factor = 2.5
        turf_sq_ft = turf_area * pixel_area * correction_factor

        logging.info(f"Calculated turf area: {turf_sq_ft} sq ft")
        return turf_sq_ft
    except Exception as e:
        logging.error(f"Error calculating turf area: {str(e)}")
        return str(e)
