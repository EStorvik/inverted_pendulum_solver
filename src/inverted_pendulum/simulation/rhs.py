import numpy as np



def rhs(x, tau, L, r, g = 9.81):
    tau_theta = tau(x)[0]
    theta = x[0]
    theta_dot = x[1]
    alpha = x[2]
    alpha_dot = x[3]
    y1 = theta_dot
    y2 = F(theta, theta_dot, alpha, alpha_dot, np.array([[tau_theta], [0]]), L, r, g)[0]
    y3 = alpha_dot
    y4 = F(theta, theta_dot, alpha, alpha_dot, np.array([[tau_theta], [0]]), L, r, g)[1]
    return np.array([y1, y2[0], y3, y4[0]])


def A(alpha, L, r):
    return np.array([[2*r**2+2*L**2/3*np.sin(alpha)**2, L*r*np.cos(alpha)],[L*r*np.cos(alpha), 2*L**2/3]])

def B(theta, theta_dot, alpha, alpha_dot, L, r, g = 9.81):
    return L*np.sin(alpha)*np.array([[4*L/3*theta_dot*alpha_dot*np.cos(alpha)-r*alpha_dot**2],[-2*L/3*theta_dot**2*np.cos(alpha)+g]])

def A_inv(alpha, L, r):
    return np.linalg.inv(A(alpha, L, r))

def F(theta, theta_dot, alpha, alpha_dot, tau, L, r, g = 9.81):
    return A_inv(alpha, L, r)@(tau-B(theta, theta_dot, alpha, alpha_dot, L, r, g))