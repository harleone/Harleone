

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from math import pi

N = 900
fps = 30
duration_sec = 12
turns_over_animation = 0.15
point_size_base = 10
point_size_gain = 80
golden_angle_deg = 137.50776405003785


BG = "#000000"
PURPLE_CORE = "#2A0436"
PURPLE_HALO = "#2A0436"
PURPLE_SPIRAL = "#a855f7"

gif_path = "fibonacci_purple.gif"

frames = int(fps * duration_sec)
golden_angle = np.deg2rad(golden_angle_deg)
phi = (1 + 5**0.5) / 2

def ease_in_out_sine(t):
    return 0.5 - 0.5 * np.cos(np.clip(t, 0, 1) * pi)

n = np.arange(1, N + 1)
base_r = np.sqrt(n)
base_r /= base_r.max()

theta_spiral = np.linspace(0, 10 * pi, 1200)
a = 0.05 
b = np.log(phi) / pi
r_spiral = a * np.exp(b * theta_spiral)

fig, ax = plt.subplots(figsize = (6, 6), dpi = 120)
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)
ax.set_aspect('equal')
ax.axis('off')
ax.set_xlim(-1.1, 1.1)
ax.set_ylim(-1.1, 1.1)

halo = ax.scatter([], [], s=[], alpha=0.15, c=PURPLE_HALO, marker='o')
core = ax.scatter([], [], s=[], alpha=0.95, c=PURPLE_CORE, marker='o')

spiral_line, = ax.plot([], [], linewidth=1.0, alpha=0.7, c=PURPLE_SPIRAL)

def init() :
    halo.set_offsets(np.empty((0, 2)))
    core.set_offsets(np.empty((0, 2)))
    halo.set_sizes([])
    core.set_sizes([])
    spiral_line.set_data([], [])
    return halo, core, spiral_line

def update(frame):
    t = frame / (frames - 1)
    grow = ease_in_out_sine(t)

    visible = max(1, int(grow * N))
    rot = 2 * pi * (turns_over_animation * t)

    theta = n[:visible] * golden_angle + rot
    r = base_r[:visible] * (0.2 + 0.8 * grow)

    x = r * np.cos(theta)
    y = r * np.sin(theta)
    offsets = np.column_stack([x, y])

    pulse = 0.5 + 0.5 * np.sin(2 * pi * (t + r))
    sizes_core = point_size_base + point_size_gain * (r ** 0.8) * pulse
    sizes_halo = sizes_core * 2.2

    halo.set_offsets(offsets)
    halo.set_sizes(sizes_halo)
    core.set_offsets(offsets)
    core.set_sizes(sizes_core)
    
    th = theta_spiral + rot
    rs = r_spiral * (0.5 + 0.5 * grow)
    xs = rs * np.cos(th)
    ys = rs * np.sin(th)
    spiral_line.set_data(xs, ys)
    
    return halo, core, spiral_line




anim = FuncAnimation(fig, update, frames=frames, init_func=init, blit=True)
writer = PillowWriter(fps=fps)
anim.save(gif_path, writer=writer)
print(f"Saved: {gif_path}")
