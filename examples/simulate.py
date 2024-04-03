import numpy as np
import inverted_pendulum as ip
import control as ct

r = 1
L = 1
g = 9.81

theta_0 = 0
theta_dot_0 = 0
alpha_dot_0 = 0
alpha_0 = 0
x0 = np.array([theta_0, theta_dot_0, alpha_0, alpha_dot_0])

# Control using the python control library
A = np.array([[0,1,0,0],[0,0,3*g/L,0],[0,0,0,1],[0,0,6*g/L,0]])
B = np.array([[0],[2/r**2],[0],[3/(L*r)]])
Q = np.eye(4)
R = np.eye(1)

control = ip.BalanceControl(x0, A, B, Q, R)

# The control input is given by tau = -Kdx, where dx is the deviation from the equilibrium point (0,0,pi,0)
tau = control.swing_up

def rhs(x):
    return ip.rhs(x, tau, r, L, g)

h = 0.01
x, t = ip.rk4(rhs, 0, x0, 20, h)

ip.visualize_with_pygame(x,h, angle_y = -np.pi/14, angle_z=np.pi/12)