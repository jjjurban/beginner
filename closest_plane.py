import requests
import math

# Haversine formula for distance (lat/lon in degrees)
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.asin(math.sqrt(a))
    return R * c

# Your location (default: Prague)
my_lat = 50.0755  # Prague latitude
my_lon = 14.4378  # Prague longitude

# Optional: Input your own coords
print("Enter your latitude (default 50.0755 for Prague): ")
lat_input = input().strip() or str(my_lat)
print("Enter your longitude (default 14.4378 for Prague): ")
lon_input = input().strip() or str(my_lon)
my_lat, my_lon = float(lat_input), float(lon_input)

print(f"Finding closest plane to ({my_lat}, {my_lon})...\n")

# Fetch plane data from OpenSky
try:
    response = requests.get("https://api.opensky-network.org/api/states/all")
    data = response.json()
except Exception as e:
    print(f"Oops, couldn’t fetch data: {e}")
    exit(1)

# Find closest plane
min_dist = float("inf")
closest_plane = None

for state in data["states"]:
    callsign = state[1].strip() or "Unknown"  # Callsign (index 1)
    lon = state[5]  # Longitude (index 5)
    lat = state[6]  # Latitude (index 6)
    if lat is None or lon is None:  # Skip if no coords
        continue
    dist = haversine(my_lat, my_lon, lat, lon)
    if dist < min_dist:
        min_dist = dist
        closest_plane = {
            "callsign": callsign,
            "lat": lat,
            "lon": lon,
            "altitude": state[7] if state[7] is not None else "N/A"  # Altitude in meters
        }

# Print result
if closest_plane:
    print(f"Closest plane: {closest_plane['callsign']}")
    print(f"Distance: {min_dist:.2f} km")
    print(f"Location: ({closest_plane['lat']}, {closest_plane['lon']})")
    print(f"Altitude: {closest_plane['altitude']} m")
else:
    print("No planes found—maybe they’re all napping!")

    