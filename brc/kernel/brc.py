import json

class BRC:
    def __init__(self, metric):
        self.metric = metric

    def evaluate(self, gamma_prev, gamma_curr, gamma_base):
        d_prev = self.metric(gamma_prev, gamma_base)
        d_curr = self.metric(gamma_curr, gamma_prev)

        R = 1 - self.metric(gamma_curr, gamma_base)
        Delta = d_curr
        S = R - Delta

        return {
            "R": R,
            "Delta": Delta,
            "S": S
        }
