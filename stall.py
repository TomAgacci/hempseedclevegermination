def omega_dirt(D):
    # D: dict with keys like 'organic', 'compaction', 'pH'
    # higher organic, moderate pH, low compaction → positive
    return (
        0.10 * D["organic"]
        - 0.08 * D["compaction"]
        - 0.05 * abs(D["pH"] - 6.5)
    )

def omega_water(W):
    # W: dict with 'moisture', 'cleanliness'
    return (
        0.15 * W["moisture"]
        - 0.10 * (1.0 - W["cleanliness"])
    )

def omega_tot(E, D, W):
    return max(0.0, omega_base(E) + omega_dirt(D) + omega_water(W))
