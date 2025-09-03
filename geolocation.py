import phonenumbers
from phonenumbers import geocoder, carrier
from opencage.geocoder import OpenCageGeocode
import folium

# Input
number = input("Enter phone number (with country code, e.g., +911234567890): ")
api_key = input("Enter your OpenCage API Key: ")

try:
    # Parse & validate number
    phone = phonenumbers.parse(number)
    if not phonenumbers.is_valid_number(phone):
        print("❌ Invalid phone number.")
        exit()

    # Get region & service provider
    region = geocoder.description_for_number(phone, "en")
    service = carrier.name_for_number(phone, "en")
    print(f"📍 Region: {region}")
    print(f"📡 Service Provider: {service}")

    # Geocode region to coordinates
    geocoder_client = OpenCageGeocode(api_key)
    result = geocoder_client.geocode(region)
    if not result:
        print("❌ Could not geocode location.")
        exit()

    lat = result[0]['geometry']['lat']
    lng = result[0]['geometry']['lng']
    print(f"🌍 Coordinates: {lat}, {lng}")

    # Generate simple map
    map_file = "location.html"
    m = folium.Map(location=[lat, lng], zoom_start=10)
    folium.Marker([lat, lng], popup=f"{region}, {service}").add_to(m)
    m.save(map_file)

    print(f"✅ Map saved as {map_file}. Open it in your browser to view.")

except Exception as e:
    print(f"⚠️ Error: {e}")
