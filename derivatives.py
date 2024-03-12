import sympy as sym

theta = sym.symbols('theta')
alpha = sym.symbols('alpha')
theta_dot = sym.symbols('dottheta')
alpha_dot = sym.symbols('dotalpha')

r = sym.symbols('r')
l = sym.symbols('ell')

x0 = sym.Matrix([[r],[0],[-l]])

R_alpha = sym.Matrix([[1, 0, 0],[0, sym.cos(alpha), -sym.sin(alpha)],[0, sym.sin(alpha), sym.cos(alpha)]])
R_theta = sym.Matrix([[sym.cos(theta), -sym.sin(theta), 0],[sym.sin(theta), sym.cos(theta), 0],[0, 0, 1]])


x = R_theta * R_alpha * x0

x_theta = x.diff(theta)
x_alpha = x.diff(alpha)

v = x_theta * theta_dot + x_alpha * alpha_dot

v_squared = v.T * v

print(x)
print(v)
print(v_squared.simplify())
