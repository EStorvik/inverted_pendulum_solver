import numpy as np
import inverted_pendulum as ip
import control as ct

# r = 0.085
# m_theta = 0.095
# m_alpha = 0.024
# L = 0.129
# g = 9.81


r = 0.1
m_theta = 0.095
m_alpha = 0.024
L = 0.1
g = 9.81

Rm = 7.5
kt = 0.042
km = kt

print(f"Voltage coefficient: {Rm/kt}")

theta_0 = 0
theta_dot_0 = 0
alpha_dot_0 = 0
alpha_0 = -np.pi/12
x0 = np.array([theta_0, theta_dot_0, alpha_0, alpha_dot_0])

# Control using the python control library
A = np.array([[0,1,0,0],[0,0,3*m_alpha*g/(4*r*(m_alpha/4+m_theta/3)),0],[0,0,0,1],[0,0, 3*g*(m_alpha+m_theta/3)/(2*L*(m_alpha/4+m_theta/3)),0]])
B = np.array([[0],[1/(r**2*(m_alpha/4+m_theta/3))],[0],[3/(2*L*r*(m_alpha/4+m_theta/3))]])
Q = 1*np.eye(4)
R = 100*np.eye(1)



control = ip.BalanceControl(x0, A, B, Q, R, k = 0.05, L = L, m_alpha = m_alpha, m_theta=m_theta, g = g)

# The control input is given by tau = -Kdx, where dx is the deviation from the equilibrium point (0,0,pi,0)
tau = control.swing_up

# def tau(x):
#     return np.array([0])

def rhs(x):
    return ip.rhs(x, tau, r, L, m_theta, m_alpha, g)

h = 0.001
x, t = ip.rk4(rhs, 0, x0, 10, h)

ip.visualize_with_pygame(x, h, angle_y = -np.pi/14, angle_z=np.pi/12)