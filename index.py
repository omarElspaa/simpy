import http.server
import socketserver
import os
import requests
import base64
import json

# Get environment variables
PORT = int(os.environ.get("PORT", 8000))
SABRE_API_KEY = os.environ.get("SABRE_API_KEY")
SABRE_API_SECRET = os.environ.get("SABRE_API_SECRET")

if not SABRE_API_KEY or not SABRE_API_SECRET:
    raise ValueError("SABRE_API_KEY and SABRE_API_SECRET must be set as environment variables")

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Request data from the Sabre Alternate Airport Shop API
        url = "https://api.sabre.com/v1/shop/flights/altairports"
        headers = {
            "Authorization": f"Bearer {self.get_sabre_token()}",
            "Content-Type": "application/json"
        }
        params = {
            "origin": "LAX",
            "destination": "JFK",
            "departuredate": "2024-07-01"
        }

        response = requests.get(url, headers=headers, params=params)
        data = response.json()

        # Prepare and send the response
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def get_sabre_token(self):
        # Obtain OAuth token from Sabre
        auth_url = "https://api.sabre.com/v2/auth/token"
        auth_headers = {
            "Authorization": f"Basic {base64.b64encode(f'{SABRE_API_KEY}:{SABRE_API_SECRET}'.encode()).decode()}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        auth_data = {
            "grant_type": "client_credentials"
        }

        auth_response = requests.post(auth_url, headers=auth_headers, data=auth_data)
        auth_response.raise_for_status()
        token_data = auth_response.json()
        return token_data['access_token']

# Start the server
with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print(f"Serving on port {PORT}")
    httpd.serve_forever()
