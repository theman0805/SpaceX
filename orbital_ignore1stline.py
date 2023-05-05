import numpy as np
import matplotlib.pyplot as plt
import requests
from datetime import datetime, timedelta
from sgp4.earth_gravity import wgs84
from sgp4.io import twoline2rv

# Load TLE data from website
url = "https://celestrak.org/NORAD/elements/starlink.txt"
tle_data = requests.get(url).text.splitlines()[1:]

# Define satellite name
sat_name = "Starlink"

# Initialize arrays for latitude and longitude
latitudes = []
longitudes = []

# Set start and end time for analysis
start_time = datetime.now()
end_time = start_time + timedelta(days=1)

# Iterate over TLE data
for i in range(0, len(tle_data), 3):
    # Parse TLE data
    line1 = tle_data[i]
    line2 = tle_data[i+1]

    # Initialize satellite
    satellite = twoline2rv(line1, line2, wgs84)

    # Iterate over time range
    curr_time = start_time
    while curr_time < end_time:
        # Get satellite position and velocity at current time
        position, velocity = satellite.propagate(
            curr_time.year, curr_time.month, curr_time.day,
            curr_time.hour, curr_time.minute, curr_time.second)

        # Calculate latitude and longitude
        latitude = np.degrees(np.arcsin(position[2]/np.linalg.norm(position)))
        longitude = np.degrees(np.arctan2(position[1], position[0]))

        # Append latitude and longitude to arrays
        latitudes.append(latitude)
        longitudes.append(longitude)

        # Increment time by 1 minute
        curr_time += timedelta(minutes=1)

# Create plot of coverage area
fig, ax = plt.subplots(figsize=(10, 10))
ax.scatter(longitudes, latitudes, s=0.1)
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")
ax.set_title(f"Coverage Area for {sat_name}")
plt.show()
