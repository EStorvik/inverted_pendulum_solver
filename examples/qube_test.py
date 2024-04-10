import inverted_pendulum as ip
import numpy as np

# Physical parameters
r = 0.1
m_theta = 0.095
m_alpha = 0.024
L = 0.1
g = 9.81

# Update frequency
hz = 1000

# Run time (in seconds)
T = 10

# Motor parameters
Rm = 7.5
kt = 0.042
km = kt

# Set the desired max voltage
max_voltage = 1

# State object (used for reading and updating current state)
states = ip.States(0, -np.pi/12, hz = hz)

# Control setup
A = np.array([[0,1,0,0],[0,0,3*m_alpha*g/(4*r*(m_alpha/4+m_theta/3)),0],[0,0,0,1],[0,0, 3*g*(m_alpha+m_theta/3)/(2*L*(m_alpha/4+m_theta/3)),0]])
B = np.array([[0],[1/(r**2*(m_alpha/4+m_theta/3))],[0],[3/(2*L*r*(m_alpha/4+m_theta/3))]])
Q = 1*np.eye(4)
R = 100*np.eye(1)

control = ip.BalanceControl(states.x, A, B, Q, R, k = 0.05, L = L, m_alpha = m_alpha, m_theta=m_theta, g = g)
torque_response = control.swing_up


def voltage_response(x, max_voltage):
    # Calculate the response in voltage of the system to the control signal, and clip it to the desired maximum voltage
    response = Rm/kt*torque_response(x)[0]
    if response > max_voltage:
        return max_voltage
    elif response < -max_voltage:
        return -max_voltage
    else:
        return response
    

def read_from_qube():
    # Read the current state from the Qube
    # TODO: Raquel
    # Should read theta and alpha from the qube and pass to the state object: states.read_states(theta, alpha)
    pass

def write_to_qube(voltage):
    # Write the control signal to the Qube (and make it act)
    # TODO: Raquel
    # Should write the control signal to the qube: voltage
    pass



for t in range(int(T*hz)):

    # Read the current state from the Qube
    read_from_qube()
    # Calculate the control signal
    voltage = voltage_response(states.x, max_voltage)
    # Write the control signal to the Qube
    write_to_qube(voltage)

