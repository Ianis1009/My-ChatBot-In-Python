import requests


NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
OSRM_URL = "https://router.project-osrm.org/route/v1/driving"

HEADERS = { "User-Agent" : "VoiceAssistant/beta"};


def geocode_city(city):
   params = {"q" : city, "format" : "json", "limit" : 1}

   try:
       response = requests.get(NOMINATIM_URL, params=params, headers=HEADERS, timeout=10)
       response.raise_for_status()
       data = response.json()
       if not data:
            return None 
       return {"name": data[0].get("display_name"), "latitude": float(data[0]["lat"]), "longitude": float(data[0]["lon"])}

   except requests.RequestException:
    return None 

def calculate_route(origin, destination):
    
    pass

