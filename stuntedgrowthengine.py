def search_min_bonsai():
    best = None
    best_E = None

    for N in [2,4,6,8]:
        for S in [2,5,10,15]:
            for T in [18,22,26]:
                for aw in [0.90,0.94,0.98]:
                    E = (N,S,T,aw)
                    J = objective(E)
                    if best is None or J < best:
                        best = J
                        best_E = E

    return best_E, best
