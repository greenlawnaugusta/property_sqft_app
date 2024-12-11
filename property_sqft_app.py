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
stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')

# Create Flask app
app = Flask(__name__)
CORS(app)

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

# Function to create Stripe product and price
def create_stripe_product_and_price(product_name, price):
    try:
        product = stripe.Product.create(name=product_name)
        stripe.Price.create(
            product=product.id,
            unit_amount=int(price * 100),  # Stripe uses cents
            currency="usd",
        )
        logging.info(f"Stripe product and price created: {product_name}")
    except Exception as e:
        logging.error(f"Error creating Stripe product and price for {product_name}: {str(e)}")

# Function to create/update GoHighLevel contact
def create_or_update_gohighlevel_contact(first_name, last_name, email, phone, address, lat, lon, pricing_info):
    try:
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
            "customFields": [
                {"name": "recurring_maintenance_biweekly_price", "value": pricing_info.get("recurring_maintenance_biweekly_price")},
                {"name": "recurring_maintenance_weekly_price", "value": pricing_info.get("recurring_maintenance_weekly_price")},
                {"name": "one_time_mow_price", "value": pricing_info.get("one_time_mow_price")},
                {"name": "full_service_biweekly_price", "value": pricing_info.get("full_service_biweekly_price")},
                {"name": "full_service_weekly_price", "value": pricing_info.get("full_service_weekly_price")},
                {"name": "turf_sq_ft", "value": pricing_info.get("turf_sq_ft")},
            ]
        }
        response = requests.post(url, headers=headers, json=contact_data)
        if response.status_code in [200, 201]:
            contact = response.json()
            logging.info("Successfully created/updated contact.")
            return contact.get("contact", {}).get("id")
        else:
            logging.error(f"Error creating/updating contact: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        logging.error(f"Error in GoHighLevel API: {str(e)}")
        return None

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.json if request.content_type == 'application/json' else request.form
        address = data.get('address')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        phone = data.get('phone')

        lat, lon = get_lat_lon(address)
        if lat is None or lon is None:
            return jsonify({"error": "Geocoding failed for the provided address."}), 400

        turf_sq_ft = calculate_turf_area(lat, lon)
        if isinstance(turf_sq_ft, str):  # If an error message was returned
            return jsonify({"error": turf_sq_ft}), 400

        pricing_info = calculate_pricing(turf_sq_ft)

        # Create Stripe products and prices
        for product_name, price in pricing_info.items():
            if product_name != "turf_sq_ft":  # Skip turf_sq_ft as it's not a price
                create_stripe_product_and_price(product_name.replace("_", " ").title(), price)

        contact_id = create_or_update_gohighlevel_contact(first_name, last_name, email, phone, address, lat, lon, pricing_info)

        return jsonify({
            "turf_sq_ft": turf_sq_ft,
            "pricing_info": pricing_info,
            "contact_id": contact_id
        })
    except Exception as e:
        logging.error(f"Error processing request: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
