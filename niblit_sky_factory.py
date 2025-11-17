# niblit_sky_factory.py
# Simulated 3D airborne factory with basic motion

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import time
import random

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_title("Niblit Sky Factory Mobile Simulation")

# Factory shape points (rectangular body)
x = [0, 180, 180, 0, 0]
y = [0, 0, 80, 80, 0]
z = [0, 0, 0, 0, 0]
ax.plot(x, y, z, color='grey')

# Core modules
core_positions = {
    "AI Core": (90, 40, 20),
    "Energy": (60, 40, 10),
    "Production": (120, 40, 5)
}
for name, (x, y, z) in core_positions.items():
    ax.scatter(x, y, z, s=50, label=name)

ax.legend()
ax.set_xlim(0, 200)
ax.set_ylim(0, 100)
ax.set_zlim(0, 80)
ax.set_xlabel('Length (m)')
ax.set_ylabel('Width (m)')
ax.set_zlabel('Altitude (m)')

plt.ion()  # interactive mode
plt.show()

# Simulate flight movement
altitude = 50
for t in range(100):
    altitude += np.sin(t / 5) * 0.5
    ax.view_init(elev=20 + np.sin(t / 10)*5, azim=t)
    plt.pause(0.05)

print("Simulation complete.")