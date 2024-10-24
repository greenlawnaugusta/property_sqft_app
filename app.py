{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyPSMZt3TmOkJ+/MyH0oQ6lk",
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/greenlawnaugusta/property_sqft_app/blob/main/app.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 1,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "mfJiSRj_viq_",
        "outputId": "05ced7cc-07e9-41a3-81ad-3faa8c30cc4e"
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
      "source": [
        "from flask import Flask, request, jsonify\n",
        "import logging\n",
        "\n",
        "# Set up logging\n",
        "logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')\n",
        "\n",
        "# Initialize Flask app\n",
        "app = Flask(__name__)\n",
        "\n",
        "# Define an API endpoint to receive address data\n",
        "@app.route('/submit-address', methods=['POST'])\n",
        "def submit_address():\n",
        "    try:\n",
        "        # Get JSON data from request\n",
        "        data = request.get_json()\n",
        "        address = data.get('address')\n",
        "\n",
        "        # Check if address is provided\n",
        "        if not address:\n",
        "            return jsonify({'error': 'Address is required'}), 400\n",
        "\n",
        "        # Here you would use the existing functions to process the address\n",
        "        # For example: lat, lon = get_lat_lon(address)\n",
        "\n",
        "        return jsonify({'message': f'Address {address} received and processing started'}), 200\n",
        "    except Exception as e:\n",
        "        logging.error(f\"Error processing request: {str(e)}\")\n",
        "        return jsonify({'error': 'An error occurred while processing the request'}), 500\n",
        "\n",
        "if __name__ == '__main__':\n",
        "    # Run the Flask app\n",
        "    app.run(host='0.0.0.0', port=5000)\n"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "C0Odcq40wFzx",
        "outputId": "81574af4-e8bc-4bfb-f7e2-b35b53281af2"
      },
      "execution_count": null,
      "outputs": [
        {
          "metadata": {
            "tags": null
          },
          "name": "stdout",
          "output_type": "stream",
          "text": [
            " * Serving Flask app '__main__'\n",
            " * Debug mode: off\n"
          ]
        },
        {
          "metadata": {
            "tags": null
          },
          "name": "stderr",
          "output_type": "stream",
          "text": [
            "INFO:werkzeug:\u001b[31m\u001b[1mWARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.\u001b[0m\n",
            " * Running on all addresses (0.0.0.0)\n",
            " * Running on http://127.0.0.1:5000\n",
            " * Running on http://172.28.0.12:5000\n",
            "INFO:werkzeug:\u001b[33mPress CTRL+C to quit\u001b[0m\n"
          ]
        }
      ]
    }
  ]
}