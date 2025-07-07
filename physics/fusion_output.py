def compute_lawson_product(tau_E, n=1e20, T=10):  # n in m⁻³, T in keV
    return n * T * tau_E  # units: keV·s/m³

def compute_fusion_power(tau_E, n=1e20, scaling=1e-23):
    return scaling * (n ** 2) * tau_E  # arbitrary units (proportional to real output)
