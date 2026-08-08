import requests

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
OSRM_URL = "https://router.project-osrm.org/route/v1/driving"

HEADERS = {
    "User-Agent": "PythonVoiceAssistant/1.0"
}


def geocode_city(city):
    city = city.strip()

    if not city:
        return None

    params = {
        "q": city,
        "format": "json",
        "limit": 1
    }

    try:
        response = requests.get(
            NOMINATIM_URL,
            params=params,
            headers=HEADERS,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        if not data:
            return None

        return {
            "name": data[0]["display_name"],
            "latitude": float(data[0]["lat"]),
            "longitude": float(data[0]["lon"])
        }

    except requests.RequestException as error:
        print("Geocoding error:", error)
        return None


def calculate_route(origin, destination):

    origin_data = geocode_city(origin)

    if origin_data is None:
        return {
            "success": False,
            "error": f"Could not find: {origin}"
        }

    destination_data = geocode_city(destination)

    if destination_data is None:
        return {
            "success": False,
            "error": f"Could not find: {destination}"
        }

    coordinates = (
        f"{origin_data['longitude']},{origin_data['latitude']};"
        f"{destination_data['longitude']},{destination_data['latitude']}"
    )

    url = f"{OSRM_URL}/{coordinates}"

    params = {
        "overview": "false",
        "steps": "false"
    }

    try:
        response = requests.get(
            url,
            params=params,
            headers=HEADERS,
            timeout=15
        )

        response.raise_for_status()

        data = response.json()

        if data.get("code") != "Ok":
            return {
                "success": False,
                "error": "Route could not be calculated."
            }

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
    

def build_route_message (route):
    # description for a calculated route
    if not route.get("success"):
        return route.get("error", "I could not calculate this route.")

    origin = route["origin"]["name"]
    destination = route["destination"]["name"]
    distance = route["distance_km"]
    duration = route["duration_hours"]

    hours = int(duration)
    minutes = round((duration - hours) * 60)
    if hours > 0 and minutes > 0:
        duration_text = f"{hours} hours and {minutes} minutes"
    elif hours > 0:
        duration_text = f"{hours} hours"
    else:
        duration_text = f"{minutes} minutes"

    message = (
        f"I calculated a route from {origin} to {destination}. "
        f"The estimated driving distance is "
        f"{distance} kilometers, "
        f"with an estimated travel time of "
        f"{duration_text}."
    )


    return message

