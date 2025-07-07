# physics/mre_solver.py

def compute_dw_dt(island, flux_surface, A, B, C, D, delta_scale=10):
    w = island.w
    q = flux_surface.q
    m = island.m
    n = island.n
    bootstrap = island.bootstrap_drive

    delta_prime = (m/n - q) * delta_scale

    if w < 1e-5:
        w = 1e-5

    return A * delta_prime + B / w + C * bootstrap - D * w**2
