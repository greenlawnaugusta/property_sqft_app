from flask import Flask, request, jsonify
import requests
import json
import logging
import os
import cv2
import numpy as np
import stripe
from flask_cors import CORS

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set API keys securely from environment variables
greenlawnaugusta_mapbox_token = os.environ.get('MAPBOX_ACCESS_TOKEN')
google_maps_api_key = os.environ.get('GOOGLE_MAPS_API_KEY')
gohighlevel_api_key = os.environ.get('GOHIGHLEVEL_API_KEY')
stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')

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
        known_lot_size = 9915
        total_pixels = mask.shape[0] * mask.shape[1]
        pixel_area = known_lot_size / total_pixels
        correction_factor = 2.5
        turf_sq_ft = turf_area * pixel_area * correction_factor

        logging.info(f"Calculated turf area: {turf_sq_ft} sq ft")
        return turf_sq_ft

    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching satellite image from Mapbox: {str(e)}")
        return f"Error fetching satellite image from Mapbox: {str(e)}"

# Function to calculate pricing
def calculate_pricing(turf_sq_ft):
    base_price = 50 if turf_sq_ft <= 4000 else 50 + np.ceil((turf_sq_ft - 4000) / 100) * 1.3

    pricing_info = {
        "recurring_maintenance_biweekly_price": base_price,
        "recurring_maintenance_weekly_price": base_price * 0.75,
        "one_time_mow_price": base_price * 1.15,
        "full_service_biweekly_price": base_price * 1.25,
        "full_service_weekly_price": base_price * 1.25 * 0.90,
        "turf_sq_ft": turf_sq_ft,
    }
    logging.info(f"Calculated pricing: {json.dumps(pricing_info, indent=4)}")
    return pricing_info

# Function to create/update GoHighLevel contact
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
        "customField": pricing_info
    }
    response = requests.post(url, headers=headers, json=contact_data)
    if response.status_code in [200, 201]:
        contact = response.json()
        logging.info("Successfully created/updated contact.")
        return contact.get("contact", {}).get("id")
    else:
        logging.error(f"Error creating/updating contact: {response.status_code} - {response.text}")
        return None

# Function to create a Stripe Checkout session
@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    data = request.json
    product_name = data.get('product_name', 'Lawn Service')
    price = data.get('price', 0)
    email = data.get('email', 'customer@example.com')

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            customer_email=email,
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': product_name,
                        },
                        'unit_amount': int(float(price) * 100),  # Convert to cents
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url='https://yourwebsite.com/success',
            cancel_url='https://yourwebsite.com/cancel',
        )
        return jsonify({'id': session.id})
    except Exception as e:
        logging.error(f"Error creating Stripe Checkout session: {str(e)}")
        return jsonify(error=str(e)), 400

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json if request.content_type == 'application/json' else request.form
    address = data.get('address')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')
    phone = data.get('phone')

    lat, lon = get_lat_lon(address)
    if lat and lon:
        turf_sq_ft = calculate_turf_area(lat, lon)
        if isinstance(turf_sq_ft, str):
            return jsonify({"error": turf_sq_ft}), 400
        pricing_info = calculate_pricing(turf_sq_ft)
        contact_id = create_or_update_gohighlevel_contact(first_name, last_name, email, phone, address, lat, lon, pricing_info)

        return jsonify({
            "turf_sq_ft": turf_sq_ft,
            "pricing_info": pricing_info,
            "contact_id": contact_id
        })
    return jsonify({"error": "Failed to process request."}), 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
