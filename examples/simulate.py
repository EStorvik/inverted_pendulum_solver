import numpy as np
import inverted_pendulum as ip


r = 1
L = 1
g = 9.81

theta_0 = 0
theta_dot_0 = 0
alpha_dot_0 = 0
alpha_0 = np.pi-np.pi/12
x0 = np.array([theta_0, theta_dot_0, alpha_0, alpha_dot_0])

def rhs(x, tau = np.array([[0], [0]])):
    return ip.rhs(x, tau, r, L, g)

x, t = ip.rk4(rhs, 0, x0, 10, 0.01)

ip.visualize_with_pygame(x,t[1]-t[0], angle_y = -np.pi/12, angle_z=np.pi/12)