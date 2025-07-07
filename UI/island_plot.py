# ui/island_plot.py

import matplotlib.pyplot as plt
import numpy as np

# Time series data
time_series = []
width_series = []
tau_E_series = []
lawson_series = []
power_series = []

def plot_island_growth(island, t, tau_E, lawson, fusion_power):
    global time_series, width_series, tau_E_series, lawson_series, power_series

    time_series.append(t)
    width_series.append(island.w)
    tau_E_series.append(tau_E)
    lawson_series.append(lawson)
    power_series.append(fusion_power)

    plt.clf()
    plt.suptitle("Magnetic Island & Fusion Performance", fontsize=14)

    # --- 1. Width vs Time ---
    ax1 = plt.subplot(2, 3, 1)
    ax1.plot(time_series, width_series, color="#1f77b4", linewidth=2, marker='o', label="Island Width")
    ax1.set_title("Island Width w(t)")
    ax1.set_xlabel("Time (t)")
    ax1.set_ylabel("w(t)")
    ax1.grid(True)

    # --- 2. Confinement Time ---
    ax2 = plt.subplot(2, 3, 2)
    ax2.plot(time_series, tau_E_series, color="#2ca02c", linewidth=2, marker='s', label="τ_E")
    ax2.set_title("Confinement Time τ_E(t)")
    ax2.set_xlabel("Time (t)")
    ax2.set_ylabel("τ_E")
    ax2.grid(True)

    # --- 3. Island Cross Section ---
    ax3 = plt.subplot(2, 3, 3)
    ax3.set_title("Island Cross Section")
    ax3.set_xlabel("x")
    ax3.set_ylabel("y")
    ax3.set_aspect('equal')
    w = island.w
    pad = 0.02
    extent = (w / 2) + pad
    ax3.set_xlim(-extent, extent)
    ax3.set_ylim(-extent, extent)
    ax3.grid(True)
    circle = plt.Circle((0, 0), radius=w / 2, color='red', fill=False)
    ax3.add_patch(circle)

    # --- 4. Fusion Power Output ---
    ax5 = plt.subplot(2, 3, 5)
    ax5.plot(
    time_series,
    power_series,
    color="#d62728",       # Red (ColorBrewer Red)
    linewidth=2,
    marker='^',
    markersize=6,
    markerfacecolor='white',
    markeredgewidth=1.5,
    label="Fusion Power"
)

    ax5.set_title("Fusion Power Output (arb. units)")
    ax5.set_xlabel("Time (t)")
    ax5.set_ylabel("Power")
    ax5.grid(True)

    plt.tight_layout()
    plt.pause(0.1)
