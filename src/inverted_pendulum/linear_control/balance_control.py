
from future import __annotations__

import numpy as np
import control as ct

class BalanceControl:
    def __init__(self, x0: np.ndarray, A: np.ndarray, B: np.ndarray, Q, R, k = 1, L = 1, r = 1, m_theta = 1, m_alpha = 1, g = 9.81):
        self.K, self.S, self.E = ct.lqr(A, B, Q, R)
        print(self.K)
        self.e = np.array([x0- np.array([0, 0, np.pi, 0])])
        self.k = k
        self.L = L
        self.r = r
        self.m_theta = m_theta
        self.m_alpha = m_alpha
        self.g = g

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
    
    def u(self, x):
        pass
    
    def reset_errors(self):
        self.e = np.array([self.e[-1]])
    

    def swing_up(self, x):
        if self.balance_position(x):
            return self.tau_P(x)
        elif np.allclose(np.array([0, 0, 0, 0]), x, atol = 0.01):
            return self.tau_P(x)
        else:
            self.reset_errors()
            return np.array([self.swing_function(x)])
        
    def swing_function(self, x):
        # E_0 = self.m_alpha*self.g*self.L
        # E = self.m_alpha*self.g*self.L/2*(1-np.cos(x[2])) + self.m_alpha/6*self.L**2*x[3]**2
        # return self.k*self.r*self.m_theta*np.sign((E-E_0)*x[3]*np.cos(x[2]))

        if x[0]< -np.pi/4 :
            return self.k*self.r*self.m_theta
        elif x[0]> np.pi/4:
            return -self.k*self.r*self.m_theta
        else:
            return -self.k*self.r*self.m_theta*np.sign(x[3]*np.cos(x[2]))

        # if x[2]*x[3]>0:
        #     return 0
        # else:
        #     return -self.k*self.r*self.m_theta*np.sign(x[3])

    def balance_position(self, x):
        if np.sign(x[2])>0:
            return (x[2]>5*np.pi/6 and x[2]<7*np.pi/6)
        else:
            return (x[2]<-5*np.pi/6 and x[2]>-7*np.pi/6)


    