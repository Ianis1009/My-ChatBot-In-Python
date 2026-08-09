import json
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

VEHICLES_FILE = os.path.join(
    BASE_DIR,
    "static",
    "data",
    "vehicles.json"
)


def load_vehicles():

    try:

        with open(
            VEHICLES_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except FileNotFoundError:

        print("[ERROR]: vehicles.json was not found.")

        return []

    except json.JSONDecodeError:

        print("[ERROR]: Invalid JSON format.")

        return []


def get_all_vehicles():

    return load_vehicles()


def get_vehicle_by_id(vehicle_id):

    vehicles = load_vehicles()

    for vehicle in vehicles:

        if vehicle["id"] == vehicle_id:
            return vehicle

    return None


def get_vehicles_by_category(category):

    vehicles = load_vehicles()

    category = category.lower()

    return [
        vehicle
        for vehicle in vehicles
        if vehicle["category"].lower() == category
    ]