import numpy as np



def rhs(x, tau, L, r, m_theta, m_alpha, g = 9.81):
    tau_theta = tau(x)[0]
    theta_dot = x[1]
    alpha = x[2]
    alpha_dot = x[3]
    y1 = theta_dot
    y2 = F(theta_dot, alpha, alpha_dot, np.array([[tau_theta], [0]]), L, r, m_theta, m_alpha, g)[0]
    y3 = alpha_dot
    y4 = F(theta_dot, alpha, alpha_dot, np.array([[tau_theta], [0]]), L, r, m_theta, m_alpha, g)[1]
    return np.array([y1, y2[0], y3, y4[0]])


def C(alpha, L, r, m_theta, m_alpha):
    return np.array([[(m_alpha+m_theta/3)*r**2+m_alpha*L**2/3*np.sin(alpha)**2, m_alpha/2*L*r*np.cos(alpha)],[m_alpha/2*L*r*np.cos(alpha), m_alpha*L**2/3]])

def D(theta_dot, alpha, alpha_dot, L, r, m_alpha, g = 9.81):
    return L*np.sin(alpha)*np.array([[2*m_alpha*L/3*theta_dot*alpha_dot*np.cos(alpha)-m_alpha/2*r*alpha_dot**2],[-m_alpha*L/3*theta_dot**2*np.cos(alpha)+m_alpha/2*g]])

def C_inv(alpha, L, r, m_theta, m_alpha):
    return np.linalg.inv(C(alpha, L, r, m_theta, m_alpha))

def F(theta_dot, alpha, alpha_dot, tau, L, r, m_theta, m_alpha, g = 9.81):
    return C_inv(alpha, L, r, m_theta, m_alpha)@(tau-D(theta_dot, alpha, alpha_dot, L, r, m_alpha, g))