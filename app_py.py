{
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/greenlawnaugusta/property_sqft_app/blob/main/app_py.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 46,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "mfJiSRj_viq_",
        "outputId": "f9070bf4-dc90-452b-b747-b156ee6ae008"
      },
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Requirement already satisfied: Flask in /usr/local/lib/python3.10/dist-packages (2.2.5)\n",
            "Requirement already satisfied: Werkzeug>=2.2.2 in /usr/local/lib/python3.10/dist-packages (from Flask) (3.0.4)\n",
            "Requirement already satisfied: Jinja2>=3.0 in /usr/local/lib/python3.10/dist-packages (from Flask) (3.1.4)\n",
            "Requirement already satisfied: itsdangerous>=2.0 in /usr/local/lib/python3.10/dist-packages (from Flask) (2.2.0)\n",
            "Requirement already satisfied: click>=8.0 in /usr/local/lib/python3.10/dist-packages (from Flask) (8.1.7)\n",
            "Requirement already satisfied: MarkupSafe>=2.0 in /usr/local/lib/python3.10/dist-packages (from Jinja2>=3.0->Flask) (3.0.2)\n"
          ]
        }
      ],
      "source": [
        "pip install Flask\n"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 47,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "X-WyrU6t-dUu",
        "outputId": "fa99658a-7e17-4533-c511-d440849f1cc0"
      },
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Requirement already satisfied: flask-cors in /usr/local/lib/python3.10/dist-packages (5.0.0)\n",
            "Requirement already satisfied: Flask>=0.9 in /usr/local/lib/python3.10/dist-packages (from flask-cors) (2.2.5)\n",
            "Requirement already satisfied: Werkzeug>=2.2.2 in /usr/local/lib/python3.10/dist-packages (from Flask>=0.9->flask-cors) (3.0.4)\n",
            "Requirement already satisfied: Jinja2>=3.0 in /usr/local/lib/python3.10/dist-packages (from Flask>=0.9->flask-cors) (3.1.4)\n",
            "Requirement already satisfied: itsdangerous>=2.0 in /usr/local/lib/python3.10/dist-packages (from Flask>=0.9->flask-cors) (2.2.0)\n",
            "Requirement already satisfied: click>=8.0 in /usr/local/lib/python3.10/dist-packages (from Flask>=0.9->flask-cors) (8.1.7)\n",
            "Requirement already satisfied: MarkupSafe>=2.0 in /usr/local/lib/python3.10/dist-packages (from Jinja2>=3.0->Flask>=0.9->flask-cors) (3.0.2)\n"
          ]
        }
      ],
      "source": [
        "pip install flask-cors\n"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 48,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "TyM4Ra8Ezbud",
        "outputId": "d34091fb-f877-4004-e621-dad4cf7927fc"
      },
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Requirement already satisfied: flask-ngrok in /usr/local/lib/python3.10/dist-packages (0.0.25)\n",
            "Requirement already satisfied: Flask>=0.8 in /usr/local/lib/python3.10/dist-packages (from flask-ngrok) (2.2.5)\n",
            "Requirement already satisfied: requests in /usr/local/lib/python3.10/dist-packages (from flask-ngrok) (2.32.3)\n",
            "Requirement already satisfied: Werkzeug>=2.2.2 in /usr/local/lib/python3.10/dist-packages (from Flask>=0.8->flask-ngrok) (3.0.4)\n",
            "Requirement already satisfied: Jinja2>=3.0 in /usr/local/lib/python3.10/dist-packages (from Flask>=0.8->flask-ngrok) (3.1.4)\n",
            "Requirement already satisfied: itsdangerous>=2.0 in /usr/local/lib/python3.10/dist-packages (from Flask>=0.8->flask-ngrok) (2.2.0)\n",
            "Requirement already satisfied: click>=8.0 in /usr/local/lib/python3.10/dist-packages (from Flask>=0.8->flask-ngrok) (8.1.7)\n",
            "Requirement already satisfied: charset-normalizer<4,>=2 in /usr/local/lib/python3.10/dist-packages (from requests->flask-ngrok) (3.4.0)\n",
            "Requirement already satisfied: idna<4,>=2.5 in /usr/local/lib/python3.10/dist-packages (from requests->flask-ngrok) (3.10)\n",
            "Requirement already satisfied: urllib3<3,>=1.21.1 in /usr/local/lib/python3.10/dist-packages (from requests->flask-ngrok) (2.2.3)\n",
            "Requirement already satisfied: certifi>=2017.4.17 in /usr/local/lib/python3.10/dist-packages (from requests->flask-ngrok) (2024.8.30)\n",
            "Requirement already satisfied: MarkupSafe>=2.0 in /usr/local/lib/python3.10/dist-packages (from Jinja2>=3.0->Flask>=0.8->flask-ngrok) (3.0.2)\n"
          ]
        }
      ],
      "source": [
        "!pip install flask-ngrok\n"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 49,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "A0UWew8wXGQX",
        "outputId": "0c2c24b4-1161-4f25-a518-4cf98929136b"
      },
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Requirement already satisfied: pyngrok in /usr/local/lib/python3.10/dist-packages (7.2.0)\n",
            "Requirement already satisfied: PyYAML>=5.1 in /usr/local/lib/python3.10/dist-packages (from pyngrok) (6.0.2)\n"
          ]
        }
      ],
      "source": [
        "!pip install pyngrok\n"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 50,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "k-pkTDKAX4HH",
        "outputId": "a5aef6da-e169-49e3-9f4e-a960d4b891aa"
      },
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Requirement already satisfied: flask-cors in /usr/local/lib/python3.10/dist-packages (5.0.0)\n",
            "Requirement already satisfied: requests in /usr/local/lib/python3.10/dist-packages (2.32.3)\n",
            "Requirement already satisfied: Flask>=0.9 in /usr/local/lib/python3.10/dist-packages (from flask-cors) (2.2.5)\n",
            "Requirement already satisfied: charset-normalizer<4,>=2 in /usr/local/lib/python3.10/dist-packages (from requests) (3.4.0)\n",
            "Requirement already satisfied: idna<4,>=2.5 in /usr/local/lib/python3.10/dist-packages (from requests) (3.10)\n",
            "Requirement already satisfied: urllib3<3,>=1.21.1 in /usr/local/lib/python3.10/dist-packages (from requests) (2.2.3)\n",
            "Requirement already satisfied: certifi>=2017.4.17 in /usr/local/lib/python3.10/dist-packages (from requests) (2024.8.30)\n",
            "Requirement already satisfied: Werkzeug>=2.2.2 in /usr/local/lib/python3.10/dist-packages (from Flask>=0.9->flask-cors) (3.0.4)\n",
            "Requirement already satisfied: Jinja2>=3.0 in /usr/local/lib/python3.10/dist-packages (from Flask>=0.9->flask-cors) (3.1.4)\n",
            "Requirement already satisfied: itsdangerous>=2.0 in /usr/local/lib/python3.10/dist-packages (from Flask>=0.9->flask-cors) (2.2.0)\n",
            "Requirement already satisfied: click>=8.0 in /usr/local/lib/python3.10/dist-packages (from Flask>=0.9->flask-cors) (8.1.7)\n",
            "Requirement already satisfied: MarkupSafe>=2.0 in /usr/local/lib/python3.10/dist-packages (from Jinja2>=3.0->Flask>=0.9->flask-cors) (3.0.2)\n"
          ]
        }
      ],
      "source": [
        "!pip install flask-cors requests\n"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 51,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "YBsutQtehqj-",
        "outputId": "da429310-50fa-4e84-cc59-7b6b8752125d"
      },
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Requirement already satisfied: ngrok in /usr/local/lib/python3.10/dist-packages (1.4.0)\n"
          ]
        }
      ],
      "source": [
        "pip install ngrok"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 52,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "WfjaqSPTiHpd",
        "outputId": "fe21c241-24be-42b7-d296-9a3b24b30ce9"
      },
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Valid configuration file at /root/.config/ngrok/ngrok.yml\n"
          ]
        }
      ],
      "source": [
        "!ngrok config check"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 53,
      "metadata": {
        "id": "fJhYBsVVtt8b"
      },
      "outputs": [],
      "source": [
        "!wget -q -O ngrok.zip https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.zip\n"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 54,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "Yo0bdsgetwLz",
        "outputId": "44c17634-2393-4e9f-a381-b8f8b919c9f3"
      },
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Archive:  ngrok.zip\n",
            "  inflating: ngrok                   \n"
          ]
        }
      ],
      "source": [
        "!unzip -o ngrok.zip\n"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 55,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "Yo9Yt9Wtty_T",
        "outputId": "3dc8e706-c341-4e17-9796-e69f7ba11324"
      },
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Authtoken saved to configuration file: /root/.config/ngrok/ngrok.yml\n"
          ]
        }
      ],
      "source": [
        "!./ngrok authtoken 2nzw0vOJwxmAtbarzAWiZTEMT5G_4B1kMmMeKoqefZ5UViMdD\n"
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "pip install nbimporter\n"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "ttHMeGe77gcH",
        "outputId": "1c94bb5e-d971-4f98-c15f-b80a75d77b81"
      },
      "execution_count": 60,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Collecting nbimporter\n",
            "  Downloading nbimporter-0.3.4-py3-none-any.whl.metadata (252 bytes)\n",
            "Downloading nbimporter-0.3.4-py3-none-any.whl (4.9 kB)\n",
            "Installing collected packages: nbimporter\n",
            "Successfully installed nbimporter-0.3.4\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "ke7OyViqX_yP",
        "outputId": "5ec6a384-d107-4783-af26-e1ddcf71fd8b"
      },
      "outputs": [
        {
          "name": "stdout",
          "output_type": "stream",
          "text": [
            "Public URL: NgrokTunnel: \"https://6a90-34-125-87-205.ngrok-free.app\" -> \"http://localhost:5000\"\n",
            " * Serving Flask app '__main__'\n",
            " * Debug mode: off\n"
          ]
        },
        {
          "name": "stderr",
          "output_type": "stream",
          "text": [
            "INFO:werkzeug:\u001b[31m\u001b[1mWARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.\u001b[0m\n",
            " * Running on http://127.0.0.1:5000\n",
            "INFO:werkzeug:\u001b[33mPress CTRL+C to quit\u001b[0m\n"
          ]
        }
      ],
      "source": [
        "from flask import Flask, request, jsonify\n",
        "from pyngrok import ngrok\n",
        "from flask_cors import CORS\n",
        "import logging\n",
        "import requests\n",
        "import cv2\n",
        "import numpy as np\n",
        "\n",
        "# Set up logging\n",
        "logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')\n",
        "\n",
        "# Set API keys\n",
        "greenlawnaugusta_mapbox_token = 'sk.eyJ1IjoiZ3JlZW5sYXduYXVndXN0YSIsImEiOiJjbTJrNWhqYXQwZDVlMmpwdzd4bDl0bGdqIn0.DFYXkt-2thT24YRg9tEdWg'\n",
        "google_maps_api_key = 'AIzaSyBOLtey3T6ug8ZBfvZl-Mu2V9kJpRtcQeo'\n",
        "gohighlevel_api_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJsb2NhdGlvbl9pZCI6InZKTk5QbW5tT3dGbzZvRFROQ0FNIiwiY29tcGFueV9pZCI6IlZGU0lKQWpDNEdQZzhLY2FuZlJuIiwidmVyc2lvbiI6MSwiaWF0IjoxNzAwNDEyNTU2OTc2LCJzdWIiOiJ1c2VyX2lkIn0.13KR3p9bWk-ImURthHgHZSJIk44MVnOMG8WjamUVf3Y'\n",
        "\n",
        "# Set up Ngrok authentication token\n",
        "ngrok.set_auth_token(\"2nzw0vOJwxmAtbarzAWiZTEMT5G_4B1kMmMeKoqefZ5UViMdD\")\n",
        "\n",
        "# Create the Flask app\n",
        "app = Flask(__name__)\n",
        "CORS(app)\n",
        "\n",
        "# Function to get latitude and longitude using Google Maps API\n",
        "def get_lat_lon(address):\n",
        "    geocoding_endpoint = f'https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={google_maps_api_key}'\n",
        "    response = requests.get(geocoding_endpoint)\n",
        "    if response.status_code == 200:\n",
        "        geocode_data = response.json()\n",
        "        if geocode_data['status'] == 'OK':\n",
        "            location = geocode_data['results'][0]['geometry']['location']\n",
        "            return location['lat'], location['lng']\n",
        "        else:\n",
        "            logging.warning(f\"Geocoding failed for address {address}: {geocode_data['status']}\")\n",
        "            return None, None\n",
        "    else:\n",
        "        logging.error(f\"Failed to fetch geocode data for address {address}: {response.status_code}\")\n",
        "        return None, None\n",
        "\n",
        "# Define an API endpoint to receive address data\n",
        "@app.route('/submit-address', methods=['POST'])\n",
        "def submit_address():\n",
        "    try:\n",
        "        # Get JSON data from request\n",
        "        data = request.get_json()\n",
        "        address = data.get('address')\n",
        "\n",
        "        if not address:\n",
        "            return jsonify({'error': 'Address is required'}), 400\n",
        "\n",
        "        # Get latitude and longitude\n",
        "        lat, lon = get_lat_lon(address)\n",
        "        if lat is None or lon is None:\n",
        "            return jsonify({'error': 'Failed to retrieve latitude and longitude'}), 500\n",
        "\n",
        "        # Assume we also have functions to calculate turf area and pricing\n",
        "        # Just for simplicity, returning the latitude and longitude here\n",
        "        response = {\n",
        "            'latitude': lat,\n",
        "            'longitude': lon\n",
        "        }\n",
        "\n",
        "        return jsonify(response), 200\n",
        "\n",
        "    except Exception as e:\n",
        "        logging.error(f\"Error processing request: {str(e)}\")\n",
        "        return jsonify({'error': 'An error occurred while processing the request'}), 500\n",
        "\n",
        "if __name__ == '__main__':\n",
        "    # Start ngrok tunnel\n",
        "    public_url = ngrok.connect(5000)\n",
        "    print(f\"Public URL: {public_url}\")\n",
        "\n",
        "    # Run the Flask app\n",
        "    app.run(port=5000)\n"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "AqSjHXwUKzdv",
        "outputId": "61ef1e9a-03d3-4aaa-fb59-81bf2fa723d8"
      },
      "outputs": [
        {
          "name": "stdout",
          "output_type": "stream",
          "text": [
            "Public URL: NgrokTunnel: \"https://131a-34-125-87-205.ngrok-free.app\" -> \"http://localhost:5000\"\n",
            " * Serving Flask app '__main__'\n",
            " * Debug mode: off\n"
          ]
        },
        {
          "name": "stderr",
          "output_type": "stream",
          "text": [
            "INFO:werkzeug:\u001b[31m\u001b[1mWARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.\u001b[0m\n",
            " * Running on http://127.0.0.1:5000\n",
            "INFO:werkzeug:\u001b[33mPress CTRL+C to quit\u001b[0m\n"
          ]
        }
      ],
      "source": [
        "from flask import Flask, request, jsonify\n",
        "from pyngrok import ngrok\n",
        "from flask_cors import CORS\n",
        "import logging\n",
        "import requests\n",
        "import cv2\n",
        "import numpy as np\n",
        "\n",
        "# Set up logging\n",
        "logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')\n",
        "\n",
        "# Set API keys\n",
        "greenlawnaugusta_mapbox_token = 'sk.eyJ1IjoiZ3JlZW5sYXduYXVndXN0YSIsImEiOiJjbTJrNWhqYXQwZDVlMmpwdzd4bDl0bGdqIn0.DFYXkt-2thT24YRg9tEdWg'\n",
        "google_maps_api_key = 'AIzaSyBOLtey3T6ug8ZBfvZl-Mu2V9kJpRtcQeo'\n",
        "gohighlevel_api_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJsb2NhdGlvbl9pZCI6InZKTk5QbW5tT3dGbzZvRFROQ0FNIiwiY29tcGFueV9pZCI6IlZGU0lKQWpDNEdQZzhLY2FuZlJuIiwidmVyc2lvbiI6MSwiaWF0IjoxNzAwNDEyNTU2OTc2LCJzdWIiOiJ1c2VyX2lkIn0.13KR3p9bWk-ImURthHgHZSJIk44MVnOMG8WjamUVf3Y'\n",
        "\n",
        "# Set up Ngrok authentication token\n",
        "ngrok.set_auth_token(\"2nzw0vOJwxmAtbarzAWiZTEMT5G_4B1kMmMeKoqefZ5UViMdD\")\n",
        "\n",
        "# Create the Flask app\n",
        "app = Flask(__name__)\n",
        "CORS(app)\n",
        "\n",
        "# Function to get latitude and longitude using Google Maps API\n",
        "def get_lat_lon(address):\n",
        "    geocoding_endpoint = f'https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={google_maps_api_key}'\n",
        "    response = requests.get(geocoding_endpoint)\n",
        "    if response.status_code == 200:\n",
        "        geocode_data = response.json()\n",
        "        if geocode_data['status'] == 'OK':\n",
        "            location = geocode_data['results'][0]['geometry']['location']\n",
        "            return location['lat'], location['lng']\n",
        "        else:\n",
        "            logging.warning(f\"Geocoding failed for address {address}: {geocode_data['status']}\")\n",
        "            return None, None\n",
        "    else:\n",
        "        logging.error(f\"Failed to fetch geocode data for address {address}: {response.status_code}\")\n",
        "        return None, None\n",
        "\n",
        "# Function to calculate turf area using a placeholder implementation\n",
        "def calculate_turf_area(lat, lon):\n",
        "    # Placeholder turf area calculation logic\n",
        "    return 5000  # Replace with actual logic for calculating turf area based on lat/lon\n",
        "\n",
        "# Function to calculate pricing based on turf area\n",
        "def calculate_pricing(turf_sq_ft):\n",
        "    # Placeholder pricing calculation logic\n",
        "    return {\n",
        "        \"service_price\": 100,  # Replace with actual pricing logic\n",
        "        \"turf_sq_ft\": turf_sq_ft\n",
        "    }\n",
        "\n",
        "# Function to create or update a contact in GoHighLevel\n",
        "def create_or_update_gohighlevel_contact(first_name, last_name, email, phone, address, lat, lon, pricing_info):\n",
        "    url = \"https://rest.gohighlevel.com/v1/contacts/\"\n",
        "    headers = {\n",
        "        \"Authorization\": f\"Bearer {gohighlevel_api_key}\",\n",
        "        \"Content-Type\": \"application/json\"\n",
        "    }\n",
        "    contact_data = {\n",
        "        \"firstName\": first_name,\n",
        "        \"lastName\": last_name,\n",
        "        \"email\": email,\n",
        "        \"phone\": phone,\n",
        "        \"address1\": address,\n",
        "        \"latitude\": lat,\n",
        "        \"longitude\": lon,\n",
        "        \"customField\": {\n",
        "            \"service_price\": pricing_info[\"service_price\"]\n",
        "        }\n",
        "    }\n",
        "\n",
        "    response = requests.post(url, headers=headers, json=contact_data)\n",
        "    if response.status_code in [200, 201]:\n",
        "        contact = response.json()\n",
        "        logging.info(\"Successfully created or updated contact in GoHighLevel with pricing information.\")\n",
        "        return contact[\"contact\"][\"id\"]\n",
        "    else:\n",
        "        logging.error(f\"Failed to create or update contact in GoHighLevel: {response.status_code} - {response.text}\")\n",
        "        return None\n",
        "\n",
        "# Define an API endpoint to receive address data\n",
        "@app.route('/submit-address', methods=['POST'])\n",
        "def submit_address():\n",
        "    try:\n",
        "        # Get JSON data from request\n",
        "        data = request.get_json()\n",
        "        address = data.get('address')\n",
        "        first_name = data.get('first_name')\n",
        "        last_name = data.get('last_name')\n",
        "        email = data.get('email')\n",
        "        phone = data.get('phone')\n",
        "\n",
        "        if not all([address, first_name, last_name, email, phone]):\n",
        "            return jsonify({'error': 'All fields are required'}), 400\n",
        "\n",
        "        # Get latitude and longitude\n",
        "        lat, lon = get_lat_lon(address)\n",
        "        if lat is None or lon is None:\n",
        "            return jsonify({'error': 'Failed to retrieve latitude and longitude'}), 500\n",
        "\n",
        "        # Calculate turf area and pricing\n",
        "        turf_sq_ft = calculate_turf_area(lat, lon)\n",
        "        pricing_info = calculate_pricing(turf_sq_ft)\n",
        "\n",
        "        # Create or update the contact in GoHighLevel\n",
        "        contact_id = create_or_update_gohighlevel_contact(first_name, last_name, email, phone, address, lat, lon, pricing_info)\n",
        "        if not contact_id:\n",
        "            return jsonify({'error': 'Failed to create or update contact'}), 500\n",
        "\n",
        "        # Prepare response\n",
        "        response = {\n",
        "            'turf_area_sq_ft': turf_sq_ft,\n",
        "            'pricing': pricing_info,\n",
        "            'contact_id': contact_id\n",
        "        }\n",
        "\n",
        "        return jsonify(response), 200\n",
        "\n",
        "    except Exception as e:\n",
        "        logging.error(f\"Error processing request: {str(e)}\")\n",
        "        return jsonify({'error': 'An error occurred while processing the request'}), 500\n",
        "\n",
        "if __name__ == '__main__':\n",
        "    # Start ngrok tunnel\n",
        "    public_url = ngrok.connect(5000)\n",
        "    print(f\"Public URL: {public_url}\")\n",
        "\n",
        "    # Run the Flask app\n",
        "    app.run(port=5000)\n"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 1,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 383
        },
        "id": "gCQpxr4TLl53",
        "outputId": "b16133ce-1264-4ca9-c672-7f5a6fac21af"
      },
      "outputs": [
        {
          "output_type": "error",
          "ename": "ModuleNotFoundError",
          "evalue": "No module named 'pyngrok'",
          "traceback": [
            "\u001b[0;31m---------------------------------------------------------------------------\u001b[0m",
            "\u001b[0;31mModuleNotFoundError\u001b[0m                       Traceback (most recent call last)",
            "\u001b[0;32m<ipython-input-1-a4f176d3a8ca>\u001b[0m in \u001b[0;36m<cell line: 2>\u001b[0;34m()\u001b[0m\n\u001b[1;32m      1\u001b[0m \u001b[0;32mfrom\u001b[0m \u001b[0mflask\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mFlask\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mrequest\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mjsonify\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m----> 2\u001b[0;31m \u001b[0;32mfrom\u001b[0m \u001b[0mpyngrok\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mngrok\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m      3\u001b[0m \u001b[0;32mfrom\u001b[0m \u001b[0mflask_cors\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mCORS\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m      4\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mlogging\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m      5\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mrequests\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;31mModuleNotFoundError\u001b[0m: No module named 'pyngrok'",
            "",
            "\u001b[0;31m---------------------------------------------------------------------------\u001b[0;32m\nNOTE: If your import is failing due to a missing package, you can\nmanually install dependencies using either !pip or !apt.\n\nTo view examples of installing some common dependencies, click the\n\"Open Examples\" button below.\n\u001b[0;31m---------------------------------------------------------------------------\u001b[0m\n"
          ],
          "errorDetails": {
            "actions": [
              {
                "action": "open_url",
                "actionText": "Open Examples",
                "url": "/notebooks/snippets/importing_libraries.ipynb"
              }
            ]
          }
        }
      ],
      "source": [
        "from flask import Flask, request, jsonify\n",
        "from pyngrok import ngrok\n",
        "from flask_cors import CORS\n",
        "import logging\n",
        "import requests\n",
        "import cv2\n",
        "import numpy as np\n",
        "\n",
        "# Set up logging\n",
        "logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')\n",
        "\n",
        "# Set API keys\n",
        "greenlawnaugusta_mapbox_token = 'sk.eyJ1IjoiZ3JlZW5sYXduYXVndXN0YSIsImEiOiJjbTJrNWhqYXQwZDVlMmpwdzd4bDl0bGdqIn0.DFYXkt-2thT24YRg9tEdWg'\n",
        "google_maps_api_key = 'AIzaSyBOLtey3T6ug8ZBfvZl-Mu2V9kJpRtcQeo'\n",
        "gohighlevel_api_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJsb2NhdGlvbl9pZCI6InZKTk5QbW5tT3dGbzZvRFROQ0FNIiwiY29tcGFueV9pZCI6IlZGU0lKQWpDNEdQZzhLY2FuZlJuIiwidmVyc2lvbiI6MSwiaWF0IjoxNzAwNDEyNTU2OTc2LCJzdWIiOiJ1c2VyX2lkIn0.13KR3p9bWk-ImURthHgHZSJIk44MVnOMG8WjamUVf3Y'\n",
        "\n",
        "# Set up Ngrok authentication token\n",
        "ngrok.set_auth_token(\"2nzw0vOJwxmAtbarzAWiZTEMT5G_4B1kMmMeKoqefZ5UViMdD\")\n",
        "\n",
        "# Create the Flask app\n",
        "app = Flask(__name__)\n",
        "CORS(app, resources={r\"/*\": {\"origins\": \"*\"}})\n",
        "\n",
        "# Function to get latitude and longitude using Google Maps API\n",
        "def get_lat_lon(address):\n",
        "    logging.info(f\"Fetching latitude and longitude for address: {address}\")\n",
        "    geocoding_endpoint = f'https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={google_maps_api_key}'\n",
        "    response = requests.get(geocoding_endpoint)\n",
        "    if response.status_code == 200:\n",
        "        geocode_data = response.json()\n",
        "        if geocode_data['status'] == 'OK':\n",
        "            location = geocode_data['results'][0]['geometry']['location']\n",
        "            logging.info(f\"Latitude and longitude found: {location['lat']}, {location['lng']}\")\n",
        "            return location['lat'], location['lng']\n",
        "        else:\n",
        "            logging.warning(f\"Geocoding failed for address {address}: {geocode_data['status']}\")\n",
        "            return None, None\n",
        "    else:\n",
        "        logging.error(f\"Failed to fetch geocode data for address {address}: {response.status_code}\")\n",
        "        return None, None\n",
        "\n",
        "# Define an API endpoint to receive address data\n",
        "@app.route('/submit-address', methods=['POST'])\n",
        "def submit_address():\n",
        "    try:\n",
        "        # Get JSON data from request\n",
        "        data = request.get_json()\n",
        "        logging.info(f\"Received data: {data}\")\n",
        "        address = data.get('address')\n",
        "        first_name = data.get('first_name')\n",
        "        last_name = data.get('last_name')\n",
        "        email = data.get('email')\n",
        "        phone = data.get('phone')\n",
        "\n",
        "        if not all([address, first_name, last_name, email, phone]):\n",
        "            logging.warning(\"Missing required fields in the request\")\n",
        "            return jsonify({'error': 'All fields are required'}), 400\n",
        "\n",
        "        # Get latitude and longitude\n",
        "        lat, lon = get_lat_lon(address)\n",
        "        if lat is None or lon is None:\n",
        "            logging.error(\"Failed to retrieve latitude and longitude\")\n",
        "            return jsonify({'error': 'Failed to retrieve latitude and longitude'}), 500\n",
        "\n",
        "        # Calculate turf area and pricing\n",
        "        logging.info(\"Calculating turf area and pricing\")\n",
        "        turf_sq_ft = calculate_turf_area(lat, lon)\n",
        "        pricing_info = calculate_pricing(turf_sq_ft)\n",
        "\n",
        "        # Create or update the contact in GoHighLevel\n",
        "        logging.info(\"Creating or updating contact in GoHighLevel\")\n",
        "        contact_id = create_or_update_gohighlevel_contact(first_name, last_name, email, phone, address, lat, lon, pricing_info)\n",
        "        if not contact_id:\n",
        "            logging.error(\"Failed to create or update contact in GoHighLevel\")\n",
        "            return jsonify({'error': 'Failed to create or update contact'}), 500\n",
        "\n",
        "        # Prepare response\n",
        "        response = {\n",
        "            'turf_area_sq_ft': turf_sq_ft,\n",
        "            'pricing': pricing_info,\n",
        "            'contact_id': contact_id\n",
        "        }\n",
        "\n",
        "        logging.info(f\"Contact created successfully: {contact_id}\")\n",
        "        return jsonify(response), 200\n",
        "\n",
        "    except Exception as e:\n",
        "        logging.error(f\"Error processing request: {str(e)}\", exc_info=True)\n",
        "        return jsonify({'error': 'An error occurred while processing the request'}), 500\n",
        "\n",
        "if __name__ == '__main__':\n",
        "    # Start ngrok tunnel\n",
        "    public_url = ngrok.connect(5000)\n",
        "    logging.info(f\"Public URL: {public_url}\")\n",
        "\n",
        "    # Run the Flask app\n",
        "    app.run(port=5000)\n"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 2,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 383
        },
        "id": "32WrEJK4RgOV",
        "outputId": "0004cb15-d82b-433a-afe9-7bca3fa5b0dc"
      },
      "outputs": [
        {
          "output_type": "error",
          "ename": "ModuleNotFoundError",
          "evalue": "No module named 'pyngrok'",
          "traceback": [
            "\u001b[0;31m---------------------------------------------------------------------------\u001b[0m",
            "\u001b[0;31mModuleNotFoundError\u001b[0m                       Traceback (most recent call last)",
            "\u001b[0;32m<ipython-input-2-2edeb19823c1>\u001b[0m in \u001b[0;36m<cell line: 2>\u001b[0;34m()\u001b[0m\n\u001b[1;32m      1\u001b[0m \u001b[0;32mfrom\u001b[0m \u001b[0mflask\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mFlask\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mrequest\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mjsonify\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m----> 2\u001b[0;31m \u001b[0;32mfrom\u001b[0m \u001b[0mpyngrok\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mngrok\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m      3\u001b[0m \u001b[0;32mfrom\u001b[0m \u001b[0mflask_cors\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mCORS\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m      4\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mlogging\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m      5\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mrequests\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;31mModuleNotFoundError\u001b[0m: No module named 'pyngrok'",
            "",
            "\u001b[0;31m---------------------------------------------------------------------------\u001b[0;32m\nNOTE: If your import is failing due to a missing package, you can\nmanually install dependencies using either !pip or !apt.\n\nTo view examples of installing some common dependencies, click the\n\"Open Examples\" button below.\n\u001b[0;31m---------------------------------------------------------------------------\u001b[0m\n"
          ],
          "errorDetails": {
            "actions": [
              {
                "action": "open_url",
                "actionText": "Open Examples",
                "url": "/notebooks/snippets/importing_libraries.ipynb"
              }
            ]
          }
        }
      ],
      "source": [
        "from flask import Flask, request, jsonify\n",
        "from pyngrok import ngrok\n",
        "from flask_cors import CORS\n",
        "import logging\n",
        "import requests\n",
        "import cv2\n",
        "import numpy as np\n",
        "\n",
        "# Set up logging\n",
        "logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')\n",
        "\n",
        "# Set API keys\n",
        "greenlawnaugusta_mapbox_token = 'sk.eyJ1IjoiZ3JlZW5sYXduYXVndXN0YSIsImEiOiJjbTJrNWhqYXQwZDVlMmpwdzd4bDl0bGdqIn0.DFYXkt-2thT24YRg9tEdWg'\n",
        "google_maps_api_key = 'AIzaSyBOLtey3T6ug8ZBfvZl-Mu2V9kJpRtcQeo'\n",
        "gohighlevel_api_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJsb2NhdGlvbl9pZCI6InZKTk5QbW5tT3dGbzZvRFROQ0FNIiwiY29tcGFueV9pZCI6IlZGU0lKQWpDNEdQZzhLY2FuZlJuIiwidmVyc2lvbiI6MSwiaWF0IjoxNzAwNDEyNTU2OTc2LCJzdWIiOiJ1c2VyX2lkIn0.13KR3p9bWk-ImURthHgHZSJIk44MVnOMG8WjamUVf3Y'\n",
        "\n",
        "# Set up Ngrok authentication token\n",
        "ngrok.set_auth_token(\"2nzw0vOJwxmAtbarzAWiZTEMT5G_4B1kMmMeKoqefZ5UViMdD\")\n",
        "\n",
        "# Create the Flask app\n",
        "app = Flask(__name__)\n",
        "CORS(app, resources={r\"/*\": {\"origins\": \"*\"}})\n",
        "\n",
        "# Function to get latitude and longitude using Google Maps API\n",
        "def get_lat_lon(address):\n",
        "    geocoding_endpoint = f'https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={google_maps_api_key}'\n",
        "    response = requests.get(geocoding_endpoint)\n",
        "    if response.status_code == 200:\n",
        "        geocode_data = response.json()\n",
        "        if geocode_data['status'] == 'OK':\n",
        "            location = geocode_data['results'][0]['geometry']['location']\n",
        "            return location['lat'], location['lng']\n",
        "        else:\n",
        "            logging.warning(f\"Geocoding failed for address {address}: {geocode_data['status']}\")\n",
        "            return None, None\n",
        "    else:\n",
        "        logging.error(f\"Failed to fetch geocode data for address {address}: {response.status_code}\")\n",
        "        return None, None\n",
        "\n",
        "# Define an API endpoint to receive address data\n",
        "@app.route('/submit-address', methods=['POST'])\n",
        "def submit_address():\n",
        "    try:\n",
        "        # Get JSON data from request\n",
        "        data = request.get_json()\n",
        "        address = data.get('address')\n",
        "        first_name = data.get('first_name')\n",
        "        last_name = data.get('last_name')\n",
        "        email = data.get('email')\n",
        "        phone = data.get('phone')\n",
        "\n",
        "        if not all([address, first_name, last_name, email, phone]):\n",
        "            return jsonify({'error': 'All fields are required'}), 400\n",
        "\n",
        "        # Get latitude and longitude\n",
        "        lat, lon = get_lat_lon(address)\n",
        "        if lat is None or lon is None:\n",
        "            return jsonify({'error': 'Failed to retrieve latitude and longitude'}), 500\n",
        "\n",
        "        # Calculate turf area and pricing\n",
        "        turf_sq_ft = calculate_turf_area(lat, lon)\n",
        "        pricing_info = calculate_pricing(turf_sq_ft)\n",
        "\n",
        "        # Create or update the contact in GoHighLevel\n",
        "        contact_id = create_or_update_gohighlevel_contact(first_name, last_name, email, phone, address, lat, lon, pricing_info)\n",
        "        if not contact_id:\n",
        "            return jsonify({'error': 'Failed to create or update contact'}), 500\n",
        "\n",
        "        # Prepare response\n",
        "        response = {\n",
        "            'turf_area_sq_ft': turf_sq_ft,\n",
        "            'pricing': pricing_info,\n",
        "            'contact_id': contact_id\n",
        "        }\n",
        "\n",
        "        return jsonify(response), 200\n",
        "\n",
        "    except Exception as e:\n",
        "        logging.error(f\"Error processing request: {str(e)}\")\n",
        "        return jsonify({'error': 'An error occurred while processing the request'}), 500\n",
        "\n",
        "if __name__ == '__main__':\n",
        "    # Start ngrok tunnel\n",
        "    public_url = ngrok.connect(5000)\n",
        "    print(f\"Public URL: {public_url}\")\n",
        "\n",
        "    # Run the Flask app\n",
        "    app.run(port=5000)\n"
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "from flask import Flask, request, jsonify\n",
        "from pyngrok import ngrok\n",
        "from flask_cors import CORS\n",
        "import logging\n",
        "import nbimporter\n",
        "import property_sqft_app as property_sqft\n",
        "\n",
        "# Set up logging\n",
        "logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')\n",
        "\n",
        "# Create the Flask app\n",
        "app = Flask(__name__)\n",
        "CORS(app, resources={r\"/*\": {\"origins\": \"*\"}})\n",
        "\n",
        "# Define an API endpoint to receive address data\n",
        "@app.route('/submit-address', methods=['POST'])\n",
        "def submit_address():\n",
        "    try:\n",
        "        # Get JSON data from request\n",
        "        data = request.get_json()\n",
        "        address = data.get('address')\n",
        "        first_name = data.get('first_name')\n",
        "        last_name = data.get('last_name')\n",
        "        email = data.get('email')\n",
        "        phone = data.get('phone')\n",
        "\n",
        "        if not all([address, first_name, last_name, email, phone]):\n",
        "            return jsonify({'error': 'All fields are required'}), 400\n",
        "\n",
        "        # Get latitude and longitude\n",
        "        lat, lon = property_sqft.get_lat_lon(address)\n",
        "        if lat is None or lon is None:\n",
        "            return jsonify({'error': 'Failed to retrieve latitude and longitude'}), 500\n",
        "\n",
        "        # Calculate turf area and pricing\n",
        "        turf_sq_ft = property_sqft.calculate_turf_area(lat, lon)\n",
        "        if isinstance(turf_sq_ft, str):\n",
        "            return jsonify({'error': turf_sq_ft}), 500  # Return error message if turf area calculation failed\n",
        "        pricing_info = property_sqft.calculate_pricing(turf_sq_ft)\n",
        "\n",
        "        # Create or update the contact in GoHighLevel\n",
        "        contact_id = property_sqft.create_or_update_gohighlevel_contact(first_name, last_name, email, phone, address, lat, lon, pricing_info)\n",
        "        if not contact_id:\n",
        "            return jsonify({'error': 'Failed to create or update contact'}), 500\n",
        "\n",
        "        # Prepare response\n",
        "        response = {\n",
        "            'turf_area_sq_ft': turf_sq_ft,\n",
        "            'pricing': pricing_info,\n",
        "            'contact_id': contact_id\n",
        "        }\n",
        "\n",
        "        return jsonify(response), 200\n",
        "\n",
        "    except Exception as e:\n",
        "        logging.error(f\"Error processing request: {str(e)}\")\n",
        "        return jsonify({'error': 'An error occurred while processing the request'}), 500\n",
        "\n",
        "if __name__ == '__main__':\n",
        "    # Start ngrok tunnel\n",
        "    public_url = ngrok.connect(5000)\n",
        "    print(f\"Public URL: {public_url}\")\n",
        "\n",
        "    # Run the Flask app\n",
        "    app.run(port=5000)\n"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 383
        },
        "id": "zcwh3zm76ibf",
        "outputId": "7122f0b6-0dd5-4b06-d48c-c392896cbf0a"
      },
      "execution_count": 3,
      "outputs": [
        {
          "output_type": "error",
          "ename": "ModuleNotFoundError",
          "evalue": "No module named 'pyngrok'",
          "traceback": [
            "\u001b[0;31m---------------------------------------------------------------------------\u001b[0m",
            "\u001b[0;31mModuleNotFoundError\u001b[0m                       Traceback (most recent call last)",
            "\u001b[0;32m<ipython-input-3-8cb463811f43>\u001b[0m in \u001b[0;36m<cell line: 2>\u001b[0;34m()\u001b[0m\n\u001b[1;32m      1\u001b[0m \u001b[0;32mfrom\u001b[0m \u001b[0mflask\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mFlask\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mrequest\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mjsonify\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m----> 2\u001b[0;31m \u001b[0;32mfrom\u001b[0m \u001b[0mpyngrok\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mngrok\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m      3\u001b[0m \u001b[0;32mfrom\u001b[0m \u001b[0mflask_cors\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mCORS\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m      4\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mlogging\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m      5\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mnbimporter\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;31mModuleNotFoundError\u001b[0m: No module named 'pyngrok'",
            "",
            "\u001b[0;31m---------------------------------------------------------------------------\u001b[0;32m\nNOTE: If your import is failing due to a missing package, you can\nmanually install dependencies using either !pip or !apt.\n\nTo view examples of installing some common dependencies, click the\n\"Open Examples\" button below.\n\u001b[0;31m---------------------------------------------------------------------------\u001b[0m\n"
          ],
          "errorDetails": {
            "actions": [
              {
                "action": "open_url",
                "actionText": "Open Examples",
                "url": "/notebooks/snippets/importing_libraries.ipynb"
              }
            ]
          }
        }
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 44,
      "metadata": {
        "id": "eeZittiuth2L"
      },
      "outputs": [],
      "source": [
        "!./ngrok http 5000\n"
      ]
    }
  ],
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyMUq24s2PUQdmZyHhU2Y4aY",
      "include_colab_link": true
    },
    "kernelspec": {
      "display_name": "Python 3",
      "name": "python3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "nbformat": 4,
  "nbformat_minor": 0
}