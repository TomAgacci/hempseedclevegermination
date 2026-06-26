# ============================================================
# PRESSURE‑CHEM FORMULA SYSTEM (FULL MODULAR ENGINE)
# ============================================================

# -----------------------------
# 1. Normalized deviation
# -----------------------------
def dev(x, x0):
    return (x - x0) / x0


# -----------------------------
# 2. Base Pressure‑Chem Operator Ω_base(E)
# -----------------------------
def omega_base(E):
    N, S, T, aw = E

    dN  = dev(N,  5.0)
    dS  = dev(S,  5.0)
    dT  = dev(T, 24.0)
    daw = dev(aw, 0.98)

    val = (
        1.0
        + 0.10*dN
        + 0.02*dS
        - 0.08*max(0, dS)
        - 0.50*(dT**2)
        + 0.50*daw
    )
    return max(0.0, min(1.5, val))


# -----------------------------
# 3. Dirt Chemistry Operator Ω_dirt(D)
# -----------------------------
def omega_dirt(D):
    # D = {organic, compaction, pH}
    return (
        0.10 * D["organic"]
        - 0.08 * D["compaction"]
        - 0.05 * abs(D["pH"] - 6.5)
    )


# -----------------------------
# 4. Microbial Pressure Operator Ω_micro(M)
# -----------------------------
def omega_micro(M):
    # M = {pressure}
    return -0.12 * M["pressure"]


# -----------------------------
# 5. Coffee‑Compound Stress Operator Ω_coffee(C)
# -----------------------------
def omega_coffee(C):
    # C = {dose}
    return -0.15 * C["dose"]


# -----------------------------
# 6. Salt‑Cycle Heat/Cool Operator Ω_cycle(X)
# -----------------------------
def omega_cycle(X):
    # X = {amplitude}
    return -0.20 * X["amplitude"]


# -----------------------------
# 7. Total Pressure‑Chem Operator Ω_tot
# -----------------------------
def omega_tot(E, D, M, C, X):
    return max(
        0.0,
        omega_base(E)
        + omega_dirt(D)
        + omega_micro(M)
        + omega_coffee(C)
        + omega_cycle(X)
    )


# -----------------------------
# 8. Mitosis Driver R_mitosis
# -----------------------------
def R_mitosis(E, D, M, C, X):
    return 1.0 * omega_tot(E, D, M, C, X)


# -----------------------------
# 9. Root–Shoot Partition π_root(t,E)
# -----------------------------
from math import exp

def pi_root(t, E):
    pi_min = 0.3
    pi_max = 0.9
    gamma  = 0.3
    return pi_min + (pi_max - pi_min) * exp(-gamma * t)


# -----------------------------
# 10. Stall + Reactivation Thresholds
# -----------------------------
R_stop    = 0.05   # stall threshold
R_restart = 0.10   # reactivation threshold


# -----------------------------
# 11. Growth Simulation with Stall + Reactivation
# -----------------------------
def simulate_growth(E_seq, D_seq, M_seq, C_seq, X_seq, days=20):
    L = 0.1
    B = 0.1
    stalled = False

    for t in range(days):
        E = E_seq[t]
        D = D_seq[t]
        M = M_seq[t]
        C = C_seq[t]
        X = X_seq[t]

        R = R_mitosis(E, D, M, C, X)

        # Stall condition
        if not stalled and R < R_stop:
            stalled = True

        # Reactivation condition
        if stalled and R >= R_restart:
            stalled = False

        if stalled:
            continue  # no growth

        # Normal growth
        pi = pi_root(t, E)
        G_root  = pi * R
        G_shoot = (1 - pi) * R

        L += 0.2 * G_root * (1 - L/5.0)
        B += 1.0 * (G_root + G_shoot)

    return L, B
