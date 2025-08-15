
import math
import requests
import httpx
import os

MAPBOX_TOKEN = os.getenv("MAPBOX_TOKEN")

def haversine(lat1, lon1, lat2, lon2):
    R = 3958.8  # Radius of earth in miles
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

async def get_driving_distance_mapbox(origin_coords: tuple, dest_coords: tuple) -> float:
    """
    Get driving distance in miles using Mapbox Directions API
    origin_coords and dest_coords are tuples: (lat, lon)
    """
    origin_lon, origin_lat = origin_coords[1], origin_coords[0]
    dest_lon, dest_lat = dest_coords[1], dest_coords[0]
    url = f"https://api.mapbox.com/directions/v5/mapbox/driving/{origin_lon},{origin_lat};{dest_lon},{dest_lat}"
    params = {
        "access_token": MAPBOX_TOKEN,
        "overview": "simplified",
        "geometries": "geojson"
    }
    
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(url, params=params)
            resp.raise_for_status()
            data = resp.json()
            # Distance is returned in meters
            distance_meters = data["routes"][0]["distance"]
            distance_miles = distance_meters * 0.000621371  # meters → miles
            return distance_miles
        except Exception as e:
            print(f"Error fetching driving distance (Mapbox): {e}")
            return None

def get_coordinates(zip_code):
    url = f"https://nominatim.openstreetmap.org/search?postalcode={zip_code}&country=USA&format=json"
    response = requests.get(url, headers={"User-Agent": "my-app"})
    response.raise_for_status()
    data = response.json()
    if not data:
        return None
    return float(data[0]["lat"]), float(data[0]["lon"])

'''
async def get_driving_distance_google(origin_coords: tuple, dest_coords: tuple) -> float:
    """
    Get driving distance in miles using Google Maps Directions API
    origin_coords and dest_coords are tuples: (lat, lon)
    """
    try:
        directions_result = gmaps.directions(
            origin=origin_coords,
            destination=dest_coords,
            mode="driving"
        )
        # Distance in meters
        distance_meters = directions_result[0]['legs'][0]['distance']['value']
        distance_miles = distance_meters * 0.000621371
        return distance_miles
    except Exception as e:
        print(f"Error fetching driving distance (Google Maps): {e}")
        return None
'''