import os
import json
import requests
import logging
import cv2
import numpy as np
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Set API keys from environment variables
greenlawnaugusta_mapbox_token = os.getenv('MAPBOX_TOKEN', 'sk.eyJ1IjoiZ3JlZW5sYXduYXVndXN0YSIsImEiOiJjbTJrNWhqYXQwZDVlMmpwdzd4bDl0bGdqIn0.DFYXkt-2thT24YRg9tEdWg')
google_maps_api_key = os.getenv('GOOGLE_MAPS_KEY', 'AIzaSyBOLtey3T6ug8ZBfvZl-Mu2V9kJpRtcQeo')
gohighlevel_api_key = os.getenv('GOHIGHLEVEL_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJsb2NhdGlvbl9pZCI6InZKTk5QbW5tT3dGbzZvRFROQ0FNIiwiY29tcGFueV9pZCI6IlZGU0lKQWpDNEdQZzhLY2FuZlJuIiwidmVyc2lvbiI6MSwiaWF0IjoxNzAwNDEyNTU2OTc2LCJzdWIiOiJ1c2VyX2lkIn0.13KR3p9bWk-ImURthHgHZSJIk44MVnOMG8WjamUVf3Y')

# Create Flask app
app = Flask(__name__)

# Configure CORS properly
CORS(app, resources={
    r"/*": {
        "origins": ["*"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization", "Access-Control-Allow-Origin"]
    }
})

@app.after_request
def after_request(response):
    """Add CORS headers to every response"""
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

def get_lat_lon(address):
    """Get latitude and longitude using Google Maps API"""
    try:
        geocoding_endpoint = f'https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={google_maps_api_key}'
        response = requests.get(geocoding_endpoint)
        response.raise_for_status()
        
        geocode_data = response.json()
        if geocode_data['status'] == 'OK':
            location = geocode_data['results'][0]['geometry']['location']
            return location['lat'], location['lng']
        else:
            logger.warning(f"Geocoding failed for address {address}: {geocode_data['status']}")
            return None, None
    except Exception as e:
        logger.error(f"Failed to fetch geocode data for address {address}: {str(e)}")
        return None, None

def calculate_turf_area(lat, lon):
    """Calculate turf area using OpenCV and Mapbox Satellite Imagery"""
    try:
        # Fetch satellite image from Mapbox Static API
        mapbox_url = f"https://api.mapbox.com/styles/v1/mapbox/satellite-v9/static/{lon},{lat},20/1000x1000?access_token={greenlawnaugusta_mapbox_token}"
        response = requests.get(mapbox_url)
        response.raise_for_status()

        # Convert response content to numpy array
        nparr = np.frombuffer(response.content, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if image is None:
            logger.error("Failed to load satellite image.")
            return None

        # Convert to HSV color space for better segmentation
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # Define color range for dormant turf (beige/tan grass)
        lower_beige = np.array([10, 0, 80])
        upper_beige = np.array([30, 100, 255])

        # Create mask and clean up
        mask = cv2.inRange(hsv_image, lower_beige, upper_beige)
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

        # Calculate area
        turf_area = cv2.countNonZero(mask)
        known_lot_size = 9915  # Lot size from manual measurement in square feet
        total_pixels = mask.shape[0] * mask.shape[1]
        pixel_area = known_lot_size / total_pixels
        turf_sq_ft = turf_area * pixel_area * 2.5  # Apply correction factor

        logger.info(f"Calculated turf area: {turf_sq_ft} sq ft")
        return turf_sq_ft

    except Exception as e:
        logger.error(f"Error calculating turf area: {str(e)}")
        return None

def calculate_pricing(turf_sq_ft):
    """Calculate pricing based on turf area"""
    try:
        # Base price calculation
        if turf_sq_ft <= 4000:
            base_price = 50
        else:
            base_price = 50 + np.ceil((turf_sq_ft - 4000) / 100) * 1.3

        # Calculate service prices
        pricing = {
            "recurring_maintenance_biweekly_price": round(base_price, 2),
            "recurring_maintenance_weekly_price": round(base_price * 0.75, 2),
            "one_time_mow_price": round(base_price * 1.15, 2),
            "full_service_biweekly_price": round(base_price * 1.25, 2),
            "full_service_weekly_price": round(base_price * 1.25 * 0.90, 2),
            "weed_control_1_price": round(base_price, 2),
            "weed_control_2_price": round(base_price * 1.10, 2),
            "weed_control_3_price": round(base_price * 1.15, 2),
            "turf_sq_ft": round(turf_sq_ft, 2)
        }

        logger.info(f"Calculated pricing: {json.dumps(pricing, indent=2)}")
        return pricing

    except Exception as e:
        logger.error(f"Error calculating pricing: {str(e)}")
        return None

def create_or_update_gohighlevel_contact(first_name, last_name, email, phone, address, lat, lon, pricing_info):
    """Create or update a contact in GoHighLevel with pricing data"""
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
            "customField": {
                "weed_control_1_price": pricing_info["weed_control_1_price"],
                "weed_control_2_price": pricing_info["weed_control_2_price"],
                "weed_control_3_price": pricing_info["weed_control_3_price"],
                "recurring_maintenance_price": pricing_info["recurring_maintenance_biweekly_price"],
                "one_time_mow_price": pricing_info["one_time_mow_price"],
                "full_service_price": pricing_info["full_service_biweekly_price"],
                "turf_sq_ft": pricing_info["turf_sq_ft"]
            }
        }

        response = requests.post(url, headers=headers, json=contact_data)
        response.raise_for_status()
        
        contact = response.json()
        logger.info("Successfully created/updated contact in GoHighLevel")
        return contact.get("contact", {}).get("id")

    except Exception as e:
        logger.error(f"Error creating/updating GoHighLevel contact: {str(e)}")
        return None

@app.route('/calculate', methods=['OPTIONS'])
def handle_options():
    """Handle OPTIONS requests for CORS preflight"""
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response, 200

@app.route('/calculate', methods=['POST'])
def calculate():
    """Main endpoint for price calculation"""
    try:
        # Log incoming request
        logger.info(f"Received request: {request.get_json()}")
        
        data = request.get_json()
        
        # Handle both full address and split address components
        address = data.get('address')
        if not address:
            # Try to construct address from components
            street = data.get('street', '')
            city = data.get('city', '')
            state = data.get('state', '')
            zip_code = data.get('zip_code', '')
            address = f"{street}, {city}, {state} {zip_code}".strip()

        if not address:
            return jsonify({
                'status': 'error',
                'message': 'Address is required',
                'data': None
            }), 400

        # Get coordinates
        lat, lon = get_lat_lon(address)
        if not lat or not lon:
            return jsonify({
                'status': 'error',
                'message': 'Could not geocode address',
                'data': None
            }), 400

        # Calculate turf area
        turf_area = calculate_turf_area(lat, lon)
        if turf_area is None:
            return jsonify({
                'status': 'error',
                'message': 'Could not calculate turf area',
                'data': None
            }), 400

        # Calculate pricing
        pricing = calculate_pricing(turf_area)
        if pricing is None:
            return jsonify({
                'status': 'error',
                'message': 'Could not calculate pricing',
                'data': None
            }), 400

        # Create/update contact if contact info provided
        if all(key in data for key in ['firstName', 'lastName', 'email', 'phone']):
            contact_id = create_or_update_gohighlevel_contact(
                data['firstName'],
                data['lastName'],
                data['email'],
                data['phone'],
                address,
                lat,
                lon,
                pricing
            )
            if contact_id:
                pricing['contact_id'] = contact_id

        # Return success response
        return jsonify({
            'status': 'success',
            'message': 'Calculation completed successfully',
            'data': pricing
        })

    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e),
            'data': None
        }), 500

# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200

# Create app instance for Gunicorn
application = app

if __name__ == '__main__':
    app.run(debug=True)
