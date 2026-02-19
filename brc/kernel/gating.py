def gate(prev_S, new_S, eps=0.05):
    dS = new_S - prev_S
    if dS >= 0:
        return True, "improve"
    if dS >= -eps:
        return True, "bounded_explore"
    return False, "reject"
