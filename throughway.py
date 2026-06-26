def omega_base(E):
    # your original N, S, T, aw operator
    ...

def omega_dirt(E, dirt):
    # compaction, organic matter, pH, etc.
    return k_dirt * dirt["stress"]

def omega_microbe(E, micro):
    # microbial load, pathogen pressure
    return k_micro * micro["pressure"]

def omega_coffee(E, coffee):
    # caffeine, acids, phenolics as stress
    return k_coffee * coffee["dose"]

def omega_saltcycle(E, cycle):
    # heat/cool + salt oscillation
    return k_cycle * cycle["amplitude"]

def omega_tot(E, dirt, micro, coffee, cycle):
    return max(
        0.0,
        omega_base(E)
        + omega_dirt(E, dirt)
        + omega_microbe(E, micro)
        + omega_coffee(E, coffee)
        + omega_saltcycle(E, cycle)
    )

def R_mitosis(E, dirt, micro, coffee, cycle):
    return 1.0 * omega_tot(E, dirt, micro, coffee, cycle)
