import math

def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great circle distance in kilometers between two points 
    on the earth specified in decimal degrees.
    """
    # Convert decimal degrees to radians 
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Haversine formula 
    dlat = lat2 - lat1 
    dlon = lon2 - lon1 
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.asin(math.sqrt(a)) 
    r = 6371.0 # Radius of earth in kilometers.
    return round(c * r, 2)

def estimate_eta_minutes(distance_km: float, speed_kmh: float = 20.0) -> int:
    """
    Estimate ETA in minutes based on distance and average speed (default 20 km/h for local responder).
    """
    if distance_km <= 0:
        return 2
    time_hours = distance_km / speed_kmh
    minutes = math.ceil(time_hours * 60)
    return max(minutes, 2)
