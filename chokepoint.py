R_stop = 0.05  # persistence threshold

def simulate_growth(E, days=20):
    L = 0.1
    B = 0.1
    for t in range(days):
        R = R_mitosis(E)
        if R < R_stop:
            # modular stop: no further growth
            break

        # normal growth update
        pi = pi_root(t, E)
        G_root  = pi * R
        G_shoot = (1-pi) * R
        L += 0.2 * G_root * (1 - L/5.0)
        B += 1.0 * (G_root + G_shoot)

    return L, B
