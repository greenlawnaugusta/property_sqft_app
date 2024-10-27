from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import os
import property_sqft_app as ps

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Create the Flask app
app = Flask(__name__)

# Enable CORS for your app with all origins to resolve CORS issues
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/')
def home():
    return "Welcome to the Property Turf Area API", 200

# Define an API endpoint to receive address and user data
@app.route('/submit-address', methods=['POST'])
def submit_address():
    try:
        data = request.get_json()
        address = data.get('address')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        phone = data.get('phone')

        if not all([address, first_name, last_name, email, phone]):
            return jsonify({'error': 'All fields are required'}), 400

        lat, lon = ps.get_lat_lon(address)
        if lat is None or lon is None:
            return jsonify({'error': 'Failed to retrieve latitude and longitude'}), 500

        turf_sq_ft = ps.calculate_turf_area(lat, lon)
        if isinstance(turf_sq_ft, str):
            return jsonify({'error': turf_sq_ft}), 500

        pricing_info = ps.calculate_pricing(turf_sq_ft)
        
        contact_id = ps.create_or_update_gohighlevel_contact(first_name, last_name, email, phone, address, lat, lon, pricing_info)
        if not contact_id:
            return jsonify({'error': 'Failed to create or update contact'}), 500

        response = {
            'turf_area_sq_ft': turf_sq_ft,
            'pricing': pricing_info,
            'contact_id': contact_id
        }

        return jsonify(response), 200

    except Exception as e:
        logging.error(f"Error processing request: {str(e)}")
        return jsonify({'error': 'An error occurred while processing the request'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
