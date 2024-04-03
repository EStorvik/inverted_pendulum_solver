
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
    
    def reset_errors(self):
        self.e = np.array([self.e[-1]])
    

    def swing_up(self, x):
        if self.balance_position(x):
            return self.tau_PID(x)
        elif np.allclose(np.array([0, 0, 0, 0]), x, atol = 0.01):
            return self.tau_P(x)
        else:
            self.reset_errors()
            return np.array([self.swing_function(x)])
        
    def swing_function(self, x, k= 10, m= 1, L = 1, g = 9.81):
        E_0 = 2*m*g*L
        E = m*g*L*(1-np.cos(x[2])) + m/6*L**2*x[3]**2
        return k*np.sign((E-E_0)*x[3]*np.cos(x[2]))

    def balance_position(self, x):
        if np.sign(x[2])>0:
            return (x[2]>5*np.pi/6 and x[2]<7*np.pi/6)
        else:
            return (x[2]<-5*np.pi/6 and x[2]>-7*np.pi/6)


    