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
stripe.api_key = os.environ.get('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')

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

# Function to create/update GoHighLevel contact
def create_or_update_gohighlevel_contact(first_name, last_name, email, phone, address, lat, lon, pricing_info):
    try:
        url = "https://rest.gohighlevel.com/v1/contacts/"
        headers = {
            "Authorization": f"Bearer {gohighlevel_api_key}",
            "Content-Type": "application/json"
        }
        # Ensure custom field names exactly match the GoHighLevel configuration
        contact_data = {
            "firstName": first_name,
            "lastName": last_name,
            "email": email,
            "phone": phone,
            "address1": address,
            "latitude": lat,
            "longitude": lon,
            "customField": {  # Match GoHighLevel custom field names exactly
                "recurring_maintenance_biweekly_price": pricing_info.get("recurring_maintenance_biweekly_price"),
                "recurring_maintenance_weekly_price": pricing_info.get("recurring_maintenance_weekly_price"),
                "one_time_mow_price": pricing_info.get("one_time_mow_price"),
                "full_service_biweekly_price": pricing_info.get("full_service_biweekly_price"),
                "full_service_weekly_price": pricing_info.get("full_service_weekly_price"),
                "weed_control_1_price": pricing_info.get("weed_control_1_price"),
                "weed_control_2_price": pricing_info.get("weed_control_2_price"),
                "weed_control_3_price": pricing_info.get("weed_control_3_price"),
                "turf_sq_ft": pricing_info.get("turf_sq_ft"),
            }
        }

        # POST request to create/update the contact in GoHighLevel
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

# Pricing Calculation Endpoint
@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.json if request.content_type == 'application/json' else request.form
        address = data.get('address')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        phone = data.get('phone')

        # Validate incoming data
        if not all([address, first_name, last_name, email, phone]):
            return jsonify({"error": "All fields are required."}), 400

        lat, lon = get_lat_lon(address)
        if lat is None or lon is None:
            return jsonify({"error": "Geocoding failed for the provided address."}), 400

        turf_sq_ft = calculate_turf_area(lat, lon)
        if isinstance(turf_sq_ft, str):  # If an error message was returned
            return jsonify({"error": turf_sq_ft}), 400

        pricing_info = calculate_pricing(turf_sq_ft)
        contact_id = create_or_update_gohighlevel_contact(first_name, last_name, email, phone, address, lat, lon, pricing_info)

        if not contact_id:
            return jsonify({"error": "Failed to create or update contact in GoHighLevel."}), 500

        return jsonify({
            "turf_sq_ft": turf_sq_ft,
            "pricing_info": pricing_info,
            "contact_id": contact_id
        })
    except Exception as e:
        logging.error(f"Error processing request: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        data = request.json
        service_price = data.get('service_price')
        customer_data = data.get('customerData')

        if not service_price or not customer_data:
            return jsonify({"error": "Service price and customer data are required."}), 400

        # Extract customer details
        first_name = customer_data.get('first_name', '')
        last_name = customer_data.get('last_name', '')
        email = customer_data.get('email', '')
        phone = customer_data.get('phone', '')
        address = customer_data.get('address', '')

        # Create GoHighLevel contact (for trigger link)
        pricing_info = calculate_pricing(customer_data.get('turf_sq_ft', 0))
        contact_id = create_or_update_gohighlevel_contact(
            first_name, last_name, email, phone, address, None, None, pricing_info
        )

        if not contact_id:
            return jsonify({"error": "Failed to create or update contact in GoHighLevel."}), 500

        # Create Stripe Customer
        customer = stripe.Customer.create(
            name=f"{first_name} {last_name}",
            email=email,
        )

        # Create Checkout Session
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {'name': 'Lawn Service'},
                    'unit_amount': int(service_price),
                },
                'quantity': 1,
            }],
            mode='payment',
            customer=customer.id,
            success_url='https://yourdomain.com/success',
            cancel_url='https://yourdomain.com/cancel',
        )

        # Generate Trigger Link
        trigger_link = (
            f"https://pricing.greenlawnaugusta.com/home-page?"
            f"contact_id={contact_id}&"
            f"first_name={first_name}&"
            f"last_name={last_name}&"
            f"email={email}&"
            f"phone={phone}&"
            f"address={address}&"
            f"turf_sq_ft={pricing_info.get('turf_sq_ft')}&"
            f"recurring_maintenance_biweekly_price={pricing_info.get('recurring_maintenance_biweekly_price')}&"
            f"recurring_maintenance_weekly_price={pricing_info.get('recurring_maintenance_weekly_price')}&"
            f"one_time_mow_price={pricing_info.get('one_time_mow_price')}&"
            f"full_service_biweekly_price={pricing_info.get('full_service_biweekly_price')}&"
            f"full_service_weekly_price={pricing_info.get('full_service_weekly_price')}&"
            f"weed_control_1_price={pricing_info.get('weed_control_1_price')}&"
            f"weed_control_2_price={pricing_info.get('weed_control_2_price')}&"
            f"weed_control_3_price={pricing_info.get('weed_control_3_price')}"
        )

        return jsonify({'session_id': session.id, 'trigger_link': trigger_link})
    except Exception as e:
        logging.error(f"Error creating checkout session: {str(e)}")
        return jsonify({'error': str(e)}), 500
