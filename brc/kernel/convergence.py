def estimate_alpha(prev_dist, new_dist):
    if prev_dist == 0:
        return 0
    return new_dist / prev_dist
