import logging
import requests
import os
import cv2
import numpy as np

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set API keys from environment variables
greenlawnaugusta_mapbox_token = os.getenv('MAPBOX_ACCESS_TOKEN')
google_maps_api_key = os.getenv('google_maps_api_key')
gohighlevel_api_key = os.getenv('go_high_level_api')

# Function to get latitude and longitude using Google Maps API
def get_lat_lon(address):
    geocoding_endpoint = f'https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={google_maps_api_key}'
    try:
        response = requests.get(geocoding_endpoint)
        response.raise_for_status()
        geocode_data = response.json()
        if geocode_data['status'] == 'OK':
            location = geocode_data['results'][0]['geometry']['location']
            return location['lat'], location['lng']
        else:
            logging.warning(f"Geocoding failed for address {address}: {geocode_data['status']}")
            return None, None
    except requests.RequestException as e:
        logging.error(f"Failed to fetch geocode data for address {address}: {str(e)}")
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
        known_lot_size = 9915  # Lot size from manual measurement in square feet
        total_pixels = mask.shape[0] * mask.shape[1]
        pixel_area = known_lot_size / total_pixels

        correction_factor = 2.5
        turf_sq_ft = turf_area * pixel_area * correction_factor

        logging.info(f"Turf area in square feet: {turf_sq_ft}")
        return turf_sq_ft

    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching satellite image from Mapbox: {str(e)}")
        return f"Error fetching satellite image from Mapbox: {str(e)}"

# Function to calculate pricing based on turf area
def calculate_pricing(turf_sq_ft):
    if turf_sq_ft <= 4000:
        price = 50
    else:
        price = 50 + np.ceil((turf_sq_ft - 4000) / 100) * 1.3

    recurring_maintenance_biweekly_price = price
    recurring_maintenance_weekly_price = recurring_maintenance_biweekly_price * 0.75
    one_time_mow_price = recurring_maintenance_biweekly_price * 1.15
    full_service_biweekly_price = recurring_maintenance_biweekly_price * 1.25
    full_service_weekly_price = full_service_biweekly_price * 0.90

    pricing_info = {
        "recurring_maintenance_weekly_price": recurring_maintenance_weekly_price,
        "recurring_maintenance_biweekly_price": recurring_maintenance_biweekly_price,
        "one_time_mow_price": one_time_mow_price,
        "full_service_weekly_price": full_service_weekly_price,
        "full_service_biweekly_price": full_service_biweekly_price
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
        "latitude": lat,
        "longitude": lon,
        "customField": {
            "recurring_maintenance_price": pricing_info["recurring_maintenance_biweekly_price"],
            "one_time_mow_price": pricing_info["one_time_mow_price"],
            "full_service_price": pricing_info["full_service_biweekly_price"]
        }
    }

    try:
        response = requests.post(url, headers=headers, json=contact_data)
        response.raise_for_status()
        contact = response.json()
        logging.info("Successfully created or updated contact in GoHighLevel.")
        return contact.get("contact", {}).get("id")
    except requests.RequestException as e:
        logging.error(f"Failed to create or update contact in GoHighLevel: {str(e)}")
        return None
