import numpy as np





class States:
    """
    Class to store the states of the inverted pendulum.
    """
    def __init__(self, theta_0, alpha_0, hz = 1000):
        self.theta = theta_0
        self.alpha = alpha_0
        self.hz = hz
        self.theta_dot = 0
        self.alpha_dot = 0
        self.x = np.array([self.theta, self.theta_dot, self.alpha, self.alpha_dot])


    def read_states(self, theta, alpha):
        self.theta_dot  = (theta - self.theta)*self.hz
        self.alpha_dot = (alpha - self.alpha)*self.hz
        self.theta = theta
        self.alpha = alpha
        self.x = np.array([self.theta, self.theta_dot, self.alpha, self.alpha_dot])