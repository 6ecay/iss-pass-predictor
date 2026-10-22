from skyfield.api import load, wgs84

city = "Frankfurt"

url = "https://celestrak.org/NORAD/elements/gp.php?CATNR=25544&FORMAT=tle"

satellites = load.tle_file(url)
iss = satellites[0]

print(iss)

ts = load.timescale()
t = ts.now()
position = iss.at(t)

ground = wgs84.subpoint_of(position)

lat = ground.latitude.degrees
lon = ground.longitude.degrees

print(f"The ISS is at latitude {lat:.2f}, and longitude {lon:.2f}")
print(f"https://earth.google.com/web/@{lat},{lon},0a,3000000d,35y,0h,0t,0r")