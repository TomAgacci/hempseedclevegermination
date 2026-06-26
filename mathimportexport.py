from math import exp

days   = 10
L_max  = 5.0      # cm
k_L    = 0.2      # cm per root growth unit
k_Br   = 1.0      # biomass per root unit
k_Bs   = 1.0      # biomass per shoot unit

# Partition parameters
pi_max = 0.9
pi_min = 0.3
gamma  = 0.3

# Initial conditions
L        = 0.1
B_root   = 0.0
B_shoot  = 0.0

def omega(E):
    # Your full Pressure Chem operator here
    return 1.0  # placeholder

def R_mitosis(E):
    R0 = 1.0
    return R0 * omega(E)

def pi_root(t):
    return pi_min + (pi_max - pi_min) * exp(-gamma * t)

E_const = (5.0, 10.0, 22.0, 0.97)

for t in range(days):
    Omega   = omega(E_const)
    R       = R_mitosis(E_const)
    G       = R

    p_root  = pi_root(t)
    G_root  = p_root * G
    G_shoot = (1.0 - p_root) * G

    # Taproot length with saturation
    growth_L = k_L * G_root * (1.0 - L / L_max)
    L       += growth_L

    # Biomass updates
    B_root  += k_Br * G_root
    B_shoot += k_Bs * G_shoot

    B_total = B_root + B_shoot

    print(
        f"Day {t+1}: pi_root={p_root:.2f}, "
        f"L={L:.3f} cm, B_root={B_root:.2f}, "
        f"B_shoot={B_shoot:.2f}, B_total={B_total:.2f}"
    )
