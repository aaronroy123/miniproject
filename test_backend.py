import sys
import os
sys.path.append(os.getcwd())

from app.app import app
import json

print("Testing /api/weather_coords endpoint...")
client = app.test_client()

# Test with valid coordinates (Kochi)
lat = 9.9312
lon = 76.2673
response = client.get(f"/api/weather_coords?lat={lat}&lon={lon}")

print(f"Status Code: {response.status_code}")
print(f"Response Body: {response.text}")

if response.status_code != 200:
    print("Request failed!")
else:
    print("Request succeeded!")
