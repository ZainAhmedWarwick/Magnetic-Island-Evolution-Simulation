# physics/confinement.py

def compute_tau_E(plasma_state, tau_E0=1.0, alpha=1.0, a=10):
    max_w = 0

    for surface in plasma_state.flux_surfaces:
        if surface.has_island():
            w = surface.magnetic_island.w
            if w > max_w:
                max_w = w

    # Clamp τ_E so it doesn't go below a floor value
    tau_E = max(tau_E0 * (1 - alpha * (max_w / a)), 0.01)
    return tau_E
