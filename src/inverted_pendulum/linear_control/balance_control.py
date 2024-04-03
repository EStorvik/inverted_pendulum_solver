
from future import __annotations__

import numpy as np
import control as ct

class BalanceControl:
    def __init__(self, x0: np.ndarray, A: np.ndarray, B: np.ndarray, Q, R):
        self.K, self.S, self.E = ct.lqr(A, B, Q, R)
        self.e = np.array([x0- np.array([0, 0, np.pi, 0])])

    def tau_P(self, x):
        return -self.K @ (x - np.array([0, 0, np.pi, 0]))
    
    def update_error(self, x):
        self.e = np.append(self.e,np.array([x- np.array([0, 0, np.pi, 0])]), axis = 0)

    def tau_PD(self, x):
        self.update_error(x)
        de = self.e[-1] - self.e[-2]
        return -self.K @ (self.e[-1] + de)
    
    def tau_PID(self, x):
        self.update_error(x)
        de = self.e[-1] - self.e[-2]
        return -self.K @ (self.e[-1] + de + np.sum(self.e, axis = 0)/len(self.e))


    