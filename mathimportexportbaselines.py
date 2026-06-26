from math import exp

# Baselines
N0, S0 = 5.0, 5.0

# Partition parameters
pi_max = 0.9
pi_min = 0.3
gamma  = 0.3
k_S    = 0.2   # salt stress → more root
k_N    = 0.2   # nitrate surplus → more shoot

def deviation(x, x0):
    return (x - x0) / x0

def pi_base(t):
    return pi_min + (pi_max - pi_min) * exp(-gamma * t)

def pi_root(t, E):
    N, S, T, aw = E
    dS = deviation(S, S0)
    dN = deviation(N, N0)

    delta_stress = k_S * max(0.0, dS) - k_N * max(0.0, dN)
    pi = pi_base(t) + delta_stress

    # clamp to [0, 1]
    return max(0.0, min(1.0, pi))

# Example regimes
E_normal   = (5.0, 5.0, 24.0, 0.98)
E_highSalt = (5.0, 12.0, 24.0, 0.98)
E_highNit  = (10.0, 5.0, 24.0, 0.98)

for t in range(0, 6):
    print(f"Day {t}:")
    print("  normal   pi_root =", round(pi_root(t, E_normal),   2))
    print("  highSalt pi_root =", round(pi_root(t, E_highSalt), 2))
    print("  highNit  pi_root =", round(pi_root(t, E_highNit),  2))
