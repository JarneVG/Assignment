# Bezier-based waypoint interpolation and visualization of the quadratic-in-z surface
# The Bezier spline is C1-continuous (tangent continuous) and locally controllable.
# We generate piecewise cubic Bezier curves using Catmull–Rom to Bezier conversion.

import numpy as np
import matplotlib.pyplot as plt

# ---------------- Waypoints ----------------
waypoints_x = np.array([7.5, 12, 30.0, 35.0, 48.0, 51.0, 62.5], dtype=float)
waypoints_z = np.array([2.5, 12.0, 12.0, 2.0, 2.0, 19.5, 17.5], dtype=float)

# ---------------- Cave polygon ----------------
cave_x = np.array([0, 15, 15, 25, 25, 55, 55, 70, 70, 45, 45, 40, 40, 0, 0], dtype=float)
cave_z = np.array([0, 0, 10, 10, -5, -5, 15, 15, 25, 25, 5, 5, 25, 25, 0], dtype=float)

# ---------------- Catmull–Rom → Bezier ----------------
def catmull_rom_to_bezier(P):
    """
    Convert Catmull–Rom control points to cubic Bezier segments.
    P: Nx2 array of waypoints
    Returns list of Bezier segments, each (P0, P1, P2, P3)
    """
    segments = []
    n = len(P)
    for i in range(n - 1):
        P0 = P[i]
        P3 = P[i + 1]

        Pm1 = P[i - 1] if i > 0 else P[i]
        Pp1 = P[i + 2] if i + 2 < n else P[i + 1]

        # Catmull–Rom to Bezier conversion
        B0 = P0
        B1 = P0 + (P3 - Pm1) / 6.0
        B2 = P3 - (Pp1 - P0) / 6.0
        B3 = P3

        segments.append((B0, B1, B2, B3))
    return segments

def bezier_eval(B, t):
    """Evaluate cubic Bezier at parameter t"""
    B0, B1, B2, B3 = B
    return (
        (1 - t)**3 * B0 +
        3 * (1 - t)**2 * t * B1 +
        3 * (1 - t) * t**2 * B2 +
        t**3 * B3
    )

# Build Bezier spline
P = np.column_stack((waypoints_x, waypoints_z))
bezier_segments = catmull_rom_to_bezier(P)

# Sample spline
samples_per_seg = 80
curve = []
for seg in bezier_segments:
    for t in np.linspace(0, 1, samples_per_seg, endpoint=False):
        curve.append(bezier_eval(seg, t))
curve.append(P[-1])
curve = np.array(curve)

x_curve = curve[:, 0]
z0_curve = curve[:, 1]

# ---------------- Surface construction ----------------
x = np.linspace(min(cave_x), max(cave_x), 350)
z = np.linspace(min(cave_z)-10, max(cave_z)+10, 250)
X, Z = np.meshgrid(x, z)

# Compute squared distance to the curve for every point in the grid
# Flatten X and Z to make points array
grid_points = np.column_stack((X.ravel(), Z.ravel()))

# Use KDTree for fast nearest neighbor search
from scipy.spatial import KDTree
tree = KDTree(curve)
dist, _ = tree.query(grid_points)
dist_sq = dist.reshape(X.shape)**2

A = 1.0
B = 1.0 # Slope for the plan1oving down in x
W = A * dist_sq - B * X 

# ---------------- Plot ----------------
fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(111, projection='3d')

ax.plot_surface(X, Z, W, linewidth=0, antialiased=True, alpha=0.85)

# Bezier valley line
ax.plot(x_curve, z0_curve, np.zeros_like(x_curve), linewidth=3)

# Waypoints
ax.scatter(waypoints_x, waypoints_z, np.zeros_like(waypoints_x), s=40)

# Cave polygon
ax.plot(cave_x, cave_z, np.zeros_like(cave_x), linewidth=3)

ax.set_xlabel("x")
ax.set_ylabel("z")
ax.set_zlabel("surface value")

plt.show()
