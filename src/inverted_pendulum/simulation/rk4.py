import numpy as np



# doing a standard RK4, fourth order explicit Runge-Kutta solver for the state-space representation of the equations

def rk4(f, t0, x0, tn, h = 0.01):
    num_steps = int((tn - t0) / h)
    tt = np.linspace(t0, tn, num_steps + 1)
    x = np.zeros((len(x0), len(tt)))
    x[:,0] = x0
    for i, t in enumerate(tt[:-1]):
        x[:,i+1] = rk4_step(f, t, x[:,i], h)
        t += h
    return x, tt

def rk4_step(f, t, x, h):
    k1 = f(t, x)
    k2 = f(t + h/2, x + h/2*k1)
    k3 = f(t + h/2, x + h/2*k2)
    k4 = f(t + h, x + h*k3)
    return x + h/6*(k1 + 2*k2 + 2*k3 + k4)
