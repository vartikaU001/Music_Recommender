import requests
import base64
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Read from environment variables
client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

def get_access_token(client_id, client_secret):
    auth_url = "https://accounts.spotify.com/api/token"
    auth_header = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode("ascii")
    headers = {
        "Authorization": f"Basic {auth_header}"
    }
    data = {
        "grant_type": "client_credentials"
    }
    response = requests.post(auth_url, headers=headers, data=data)

    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        print("Error fetching access token:", response.json())
        return None

access_token = get_access_token(client_id, client_secret)
print(f"Access Token: {access_token}")
