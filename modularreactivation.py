R_stop    = 0.05
R_restart = 0.10

def simulate_growth(E_seq, D_seq, W_seq, days=20):
    L = 0.1
    B = 0.1
    stalled = False

    for t in range(days):
        E = E_seq[t]
        D = D_seq[t]
        W = W_seq[t]

        R = R_mitosis(E, D, W)

        if not stalled and R < R_stop:
            stalled = True  # enter bonsai stall

        if stalled and R >= R_restart:
            stalled = False  # modular reactivation

        if stalled:
            # no growth while stalled
            continue

        # normal growth when active
        pi = pi_root(t, E)
        G_root  = pi * R
        G_shoot = (1-pi) * R
        L += 0.2 * G_root * (1 - L/5.0)
        B += 1.0 * (G_root + G_shoot)

    return L, B
