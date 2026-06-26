from math import exp

# Baselines
N0, S0, T0, aw0 = 5.0, 5.0, 24.0, 0.98
P_germ0    = 0.80
R_mitosis0 = 1.00

# Coefficients
alpha_N = 0.10
alpha_S = 0.02
beta_S  = 0.08
beta_T  = 0.50
alpha_w = 0.50
OMEGA_MAX = 1.5

pi_max = 0.9
pi_min = 0.3
gamma  = 0.3
k_S    = 0.2
k_N    = 0.2

def deviation(x, x0):
    return (x - x0) / x0

def omega(E):
    N, S, T, aw = E
    dN  = deviation(N,  N0)
    dS  = deviation(S,  S0)
    dT  = deviation(T,  T0)
    daw = deviation(aw, aw0)

    val = (
        1.0
        + alpha_N * dN
        + alpha_S * dS
        - beta_S  * max(0.0, dS)
        - beta_T  * (dT ** 2)
        + alpha_w * daw
    )
    return max(0.0, min(OMEGA_MAX, val))

def P_germ(E):
    return P_germ0 * omega(E)

def R_mitosis(E):
    return R_mitosis0 * omega(E)

def pi_base(t):
    return pi_min + (pi_max - pi_min) * exp(-gamma * t)

def pi_root(t, E):
    N, S, T, aw = E
    dS = deviation(S, S0)
    dN = deviation(N, N0)
    delta_stress = k_S * max(0.0, dS) - k_N * max(0.0, dN)
    pi = pi_base(t) + delta_stress
    return max(0.0, min(1.0, pi))

def sweep_plugin(N_range, S_range, T_range, aw_range, t_probe=2):
    results = []
    for N in N_range:
        for S in S_range:
            for T in T_range:
                for aw in aw_range:
                    E = (N, S, T, aw)
                    Om   = omega(E)
                    Pg   = P_germ(E)
                    Rm   = R_mitosis(E)
                    pi_r = pi_root(t_probe, E)
                    results.append({
                        "E": E,
                        "Omega": Om,
                        "P_germ": Pg,
                        "R_mitosis": Rm,
                        "pi_root": pi_r,
                    })
    # sort by Omega or any metric you want
    results.sort(key=lambda r: r["Omega"], reverse=True)
    return results

# Example usage
N_range  = [3.0, 5.0, 7.0, 9.0]
S_range  = [3.0, 5.0, 8.0, 12.0]
T_range  = [20.0, 24.0, 28.0]
aw_range = [0.95, 0.97, 0.99]

top = sweep_plugin(N_range, S_range, T_range, aw_range)[0]
print("Max Omega environment:", top["E"])
print("Omega =", round(top["Omega"], 3),
      "P_germ =", round(top["P_germ"], 3),
      "R_mitosis =", round(top["R_mitosis"], 3),
      "pi_root =", round(top["pi_root"], 3))
