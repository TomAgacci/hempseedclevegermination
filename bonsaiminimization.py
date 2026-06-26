def simulate_growth(E, days=20):
    L = 0.1
    B = 0.1
    L_max = 5.0
    k_L = 0.2
    k_B = 1.0

    for t in range(days):
        R = R_mitosis(E)
        pi = 0.3 + 0.6 * (2.71828**(-0.3*t))  # root-heavy early

        G_root  = pi * R
        G_shoot = (1-pi) * R

        L += k_L * G_root * (1 - L/L_max)
        B += k_B * (G_root + G_shoot)

    return L, B

def objective(E):
    L, B = simulate_growth(E)
    return 0.7*L + 0.3*B
