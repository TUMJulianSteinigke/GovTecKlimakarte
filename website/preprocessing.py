import json
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

# Initialize the geolocator
geolocator = Nominatim(user_agent="geojson_preprocessor")

# Function to perform reverse geocoding with retries
def reverse_geocode(lat, lon):
    try:
        location = geolocator.reverse((lat, lon), language="en")
        district = location.raw.get("address", {}).get("suburb", "Unknown District")
        return district
    except GeocoderTimedOut:
        return "Unknown District"

# Load GeoJSON file
input_geojson_path = "heatLevel1.geojson"
output_geojson_path = "heatLevel1_with_distr.geojson"

with open(input_geojson_path, "r") as f:
    geojson_data = json.load(f)
# Process each feature
for feature in geojson_data["features"]:
    # Get the first coordinate of the polygon
    coordinates = feature["geometry"]["coordinates"][0][0]  # Adjust if GeoJSON structure differs
    lat, lon = coordinates[1], coordinates[0]  # Latitude, Longitude

    # Reverse geocode to get the district
    district = reverse_geocode(lat, lon)
    print(f"Processed: {district} for coordinates: {lat}, {lon}")

    # Add district to the feature's properties
    feature["properties"]["district"] = district

# Save the updated GeoJSON
with open(output_geojson_path, "w") as f:
    json.dump(geojson_data, f)

print(f"GeoJSON preprocessing complete. Saved to {output_geojson_path}")
