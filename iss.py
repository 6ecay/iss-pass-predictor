from skyfield.api import load, wgs84
import reverse_geocoder as rg
from geopy.geocoders import Nominatim

url = "https://celestrak.org/NORAD/elements/gp.php?CATNR=25544&FORMAT=tle"

satellites = load.tle_file(url)
iss = satellites[0]

ts = load.timescale()
t = ts.now()
position = iss.at(t)

ground = wgs84.subpoint_of(position)

lat = float(ground.latitude.degrees)
lon = float(ground.longitude.degrees)

places = rg.search((lat, lon), mode=1, verbose=False)
place = places[0]

geolocator = Nominatim(user_agent="iss-pass-predictor")
city = input("What City to look up? ")
location = geolocator.geocode(city, language="en")

print(f"City to look up: {location}")

observer = wgs84.latlon(location.latitude, location.longitude)
t_end = t + 7
times, events = iss.find_events(observer, t, t_end, altitude_degrees=10.0)

for ti, event in zip(times, events):
    if event == 0:
        print(f"Next pass over {city}: {ti.utc_strftime()}")
        break

print()
print("-" * 40)
print()
print("General information")
print()

print(f"The ISS is at latitude {lat:.4f}, and longitude {lon:.4f}")

if place['admin1']:
    print(f"Nearest place: {place['name']}, {place['admin1']}, {place['cc']}")
else:
    print(f"Nearest place: {place['name']}, {place['cc']}")

print(f"Map: https://earth.google.com/web/@{lat},{lon},0a,3000000d,35y,0h,0t,0r")