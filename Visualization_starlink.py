import requests
from sgp4.earth_gravity import wgs84
from sgp4.io import twoline2rv
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

url = "https://celestrak.org/NORAD/elements/starlink.txt"
response = requests.get(url)
content = response.text

# Split the content into individual TLEs
tles = content.strip().split("\n")

# Parse the first TLE
name, line1, line2 = tles[0], tles[1], tles[2]
satellite = twoline2rv(line1, line2, wgs84)

# Compute the satellite's position and velocity over time
from datetime import datetime, timedelta
start_time = datetime.utcnow()
end_time = start_time + timedelta(days=1)
delta_t = timedelta(minutes=10)

positions = []
while start_time < end_time:
    position, _ = satellite.propagate(start_time.year, start_time.month, start_time.day, start_time.hour, start_time.minute, start_time.second)
    positions.append(position)
    start_time += delta_t

# Create a 3D plot of the satellite's orbital trajectory
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.plot([pos[0] for pos in positions], [pos[1] for pos in positions], [pos[2] for pos in positions])
plt.show()
