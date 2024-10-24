# -*- coding: utf-8 -*-
"""property_sqft_app.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1W9m3qn8sKTw6lbsiQcgNs8QFTqmcjU7E
"""

import subprocess
import os

# Install required packages
subprocess.run(["pip", "install", "cartopy", "requests", "opencv-python", "numpy"])

import requests
import json
import logging
import cv2
import numpy as np

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set Mapbox tokens
greenlawnaugusta_mapbox_token = 'sk.eyJ1IjoiZ3JlZW5sYXduYXVndXN0YSIsImEiOiJjbTJrNWhqYXQwZDVlMmpwdzd4bDl0bGdqIn0.DFYXkt-2thT24YRg9tEdWg'
default_public_token = 'pk.eyJ1IjoiZ3JlZW5sYXduYXVndXN0YSIsImEiOiJjbTJrNTF1em0wY21nMnJweHUyNHFzZTNjIn0.qQ3wR4h3CMR9BA1mKSURcA'

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

        logging.info(f"Turf area in square feet: {turf_sq_ft}")
        logging.info(f"Estimated price for Recurring Maintenance: ${recurring_maintenance_price:.2f}")
        logging.info(f"Estimated price for One Time Mow: ${one_time_mow_price:.2f}")
        logging.info(f"Estimated price for Full Service: ${full_service_price:.2f}")
        logging.info(f"Estimated price for Weed Control 1: ${weed_control_1_price:.2f}")
        logging.info(f"Estimated price for Weed Control 2: ${weed_control_2_price:.2f}")
        logging.info(f"Estimated price for Weed Control 3: ${weed_control_3_price:.2f}")

        # Display Google Street View image
        google_maps_api_key = 'AIzaSyBOLtey3T6ug8ZBfvZl-Mu2V9kJpRtcQeo'
        street_view_url = f"https://maps.googleapis.com/maps/api/streetview?size=600x400&location={lat},{lon}&key={google_maps_api_key}"
        response_street_view = requests.get(street_view_url)
        response_street_view.raise_for_status()
        street_view_image_path = 'street_view_image.png'
        with open(street_view_image_path, 'wb') as f:
            f.write(response_street_view.content)

        # Log the street view image path
        logging.info(f"Street view image saved at: {street_view_image_path}")

        return (f"{turf_sq_ft:.2f} square feet\n"
                f"Estimated price for Recurring Maintenance: ${recurring_maintenance_price:.2f}\n"
                f"Estimated price for One Time Mow: ${one_time_mow_price:.2f}\n"
                f"Estimated price for Full Service: ${full_service_price:.2f}\n"
                f"Estimated price for Weed Control 1: ${weed_control_1_price:.2f}\n"
                f"Estimated price for Weed Control 2: ${weed_control_2_price:.2f}\n"
                f"Estimated price for Weed Control 3: ${weed_control_3_price:.2f}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching satellite image from Mapbox: {str(e)}")
        return f"Error fetching satellite image from Mapbox: {str(e)}"

if __name__ == '__main__':
    address = os.getenv("ADDRESS", "4496 Galway Drive, Evans, GA 30809")  # Use environment variable or default address
    lat, lon = get_lat_lon(address)
    if lat is not None and lon is not None:
        turf_sq_ft = calculate_turf_area(lat, lon)
        print(f"Estimated turf area: {turf_sq_ft}")
    else:
        print("Failed to retrieve latitude and longitude for the address.")
