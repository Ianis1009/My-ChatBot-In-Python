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

    origin_data = geocode_city(origin)

    if origin_data is None:
        return {
            "success": False,
            "error": f"Could not find origin: {origin}"
        }

    destination_data = geocode_city(destination)

    if destination_data is None:
        return {
            "success": False,
            "error": f"Could not find destination: {destination}"
        }
    origin_coordinates = (f"{origin_data['longitude']}, " f"{origin_data['latitude']}")
    destination_coordinates = (
        f"{destination_data['longitude']},"
        f"{destination_data['latitude']}"
    )

    route_url = (
        f"{OSRM_URL}/"
        f"{origin_coordinates};"
        f"{destination_coordinates}"
    )

    params = {
        "overview": "false",
        "steps": "false"
    }

    try: 
        response = requests.get(route_url, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
        if data.get("code") != "Ok":
            return {"succes":False, 
                    "error": "Could not calculate the route."}
        route = data["routes"][0]
        distance_km = route["distance"] / 1000
        duration_hours = route["duration"] / 3600

        return {
            "success": True,
            "origin": origin_data,
            "destination": destination_data,
            "distance_km": round(distance_km, 1),
            "duration_hours": round(duration_hours, 1)
        }

    except requests.RequestException as error:

        return {
            "success": False,
            "error": str(error)
        }


