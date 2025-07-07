from plasma.flux_surface import FluxSurface, MagneticIsland
from plasma.plasma_state import PlasmaState
from physics.mre_solver import compute_dw_dt
from physics.confinement import compute_tau_E
from physics.fusion_output import compute_lawson_product, compute_fusion_power
from UI.island_plot import plot_island_growth
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
import time

#Global variables
plasma_state = None
target_island = None

plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'font.size': 11,
    'axes.titleweight': 'bold',
    'axes.labelweight': 'bold',
    'axes.titlesize': 14,
    'axes.labelsize': 12,
})

#Parameters that the user will change and experiment with 
params = {
    "bootstrap": 0.2,
    "delta_scale": 10,
    "D": 1.0,
    "initial_width": 0.01
}

#Building the intial plasma for the given experiement
def build_initial_plasma():
    global plasma_state, target_island
    flux_surfaces = []
    target_island = None

    for r in range(1, 11):
        radius = r
        q = 1 + 0.1 * r

        if abs(q - 2.0) < 0.05:
            island = MagneticIsland(
                w0=params["initial_width"],
                m=2,
                n=1,
                bootstrap_drive=params["bootstrap"]
            )
            target_island = island
        else:
            island = None

        surface = FluxSurface(radius=radius, q=q, magnetic_island=island)
        flux_surfaces.append(surface)

    plasma_state = PlasmaState(flux_surfaces)
    print(f"Initialized island with w₀ = {target_island.w}, bootstrap = {params['bootstrap']}, Δ′ scale = {params['delta_scale']}, D = {params['D']}")


def run_simulation(event=None):
    global plasma_state, target_island
    build_initial_plasma()

    dt = 0.1
    steps = 50
    plt.ion()
    fig = plt.figure(figsize=(15, 8))

    powers = []

    for t in range(steps):
        plasma_state.evolve_islands(
            dt,
            lambda isl, fs: compute_dw_dt(isl, fs, A=0.5, B=0.01, C=0.5, D=params["D"], delta_scale=params["delta_scale"])
        )

        tau_E = compute_tau_E(plasma_state)
        lawson = compute_lawson_product(tau_E)
        power = compute_fusion_power(tau_E)
        powers.append(power)

        plot_island_growth(target_island, t * dt, tau_E, lawson, power)
        time.sleep(0.05)

    plt.ioff()


    final_width = target_island.w
    cross_section_radius = final_width / 2
    final_power = powers[-1]

    # Estimate gradient of fusion power (last 5 steps)
    if len(powers) >= 6:
        dP_dt = (powers[-1] - powers[-6]) / (dt * 5)
    else:
        dP_dt = 0

    print("\n--- FINAL SIMULATION OUTPUT ---")
    print(f"Final Island Width (w): {final_width:.5f}")
    print(f"Island Cross-Section Radius: {cross_section_radius:.5f}")
    print(f"Final Fusion Power Output: {final_power:.3e} (arb. units)")
    print(f"Estimated dPower/dt: {dP_dt:.3e} (arb. units/s)")



def build_ui():
    fig, _ = plt.subplots()
    plt.subplots_adjust(left=0.3, bottom=0.5)
    plt.axis('off')

    # --- SLIDERS ---
    ax_w0 = plt.axes([0.35, 0.35, 0.5, 0.03])
    ax_bootstrap = plt.axes([0.35, 0.30, 0.5, 0.03])
    ax_delta = plt.axes([0.35, 0.25, 0.5, 0.03])
    ax_d = plt.axes([0.35, 0.20, 0.5, 0.03])

    s_w0 = Slider(ax_w0, 'Initial Width', 0.001, 0.05, valinit=params["initial_width"])
    s_bootstrap = Slider(ax_bootstrap, 'Bootstrap Drive', 0.0, 1.0, valinit=params["bootstrap"])
    s_delta = Slider(ax_delta, 'Δ′ Scale', 0.0, 20.0, valinit=params["delta_scale"])
    s_d = Slider(ax_d, 'D (Saturation)', 0.1, 2.0, valinit=params["D"])

    # --- BUTTON ---
    ax_button = plt.axes([0.4, 0.1, 0.2, 0.05])
    b_run = Button(ax_button, 'Run Simulation')

    def update(val):
        params["initial_width"] = s_w0.val
        params["bootstrap"] = s_bootstrap.val
        params["delta_scale"] = s_delta.val
        params["D"] = s_d.val

    s_w0.on_changed(update)
    s_bootstrap.on_changed(update)
    s_delta.on_changed(update)
    s_d.on_changed(update)
    b_run.on_clicked(run_simulation)

    plt.show()

if __name__ == "__main__":
    build_ui()

