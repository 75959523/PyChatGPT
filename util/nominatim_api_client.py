import requests

NOMINATIM_API_BASE_URL = "https://nominatim.openstreetmap.org"


def reverse_geocode(lat, lon, zoom):
    url = f"{NOMINATIM_API_BASE_URL}/reverse?lat={lat}&lon={lon}&zoom={zoom}&format=json"
    response = requests.get(url)
    return response.text
