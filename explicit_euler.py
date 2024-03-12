import numpy as np
import matplotlib.pyplot as plt


import pygame
import sys
import math

import robolie as rl

# Model parameters
L = 1
r = 1
m_h = 1
m_v = 1
g = 9.81

# Discretization parameters
dt = 0.001
time_steps = 100000
t = 0

# Initial conditions
theta = 0
v = 0
v_dot = 0
alpha = -np.pi+np.pi/4
u = 0
u_dot = 0

def tau_theta(t):
    return 0

def F_theta(v, alpha, u, u_dot, tau_theta = 0):
    return (tau_theta-(4*L**2)/3*u*v*np.sin(alpha)*np.cos(alpha)+L*r*(u_dot*np.cos(alpha)-u**2*np.sin(alpha)))/((2*L**2)/(3)*np.sin(alpha)**2+2*r**2)

def F_alpha(v, v_dot, alpha, u, tau_alpha = 0):
    return (tau_alpha + (2*L**2)/(3)*v**2*np.sin(alpha)*np.cos(alpha)-L*u*v*r*np.sin(alpha)-L*g*np.sin(alpha)-L*r*(v_dot*np.cos(alpha)-v*u*np.sin(alpha)))/((2*L**2)/(3))

theta_list = []
alpha_list = []

for i in range(time_steps):
    v_dot = F_theta(v, alpha, u, u_dot, tau_theta=tau_theta(t))
    u_dot = F_alpha(v, v_dot, alpha, u)
    
    t += dt

    theta += v*dt
    alpha += u*dt
    v += F_theta(v, alpha, u, u_dot, tau_theta=tau_theta(t))*dt
    u += F_alpha(v, v_dot, alpha, u)*dt

    theta_list.append(theta)
    alpha_list.append(alpha)




# Constants
WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (255, 255, 255)
BEAM_COLOR = (0, 0, 255)
PENDULUM_COLOR = (255, 0, 0)
FPS = int(1/dt)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption('Furuta Pendulum Simulation')

# Pendulum settings
beam_length = 100  # Length of the horizontal beam
pendulum_length = 100  # Length of the pendulum
ball_radius = 10  # Radius of the pendulum ball

# Stationary point
sp = np.array([beam_length, 0, -pendulum_length])

# Sample data (replace with your own lists)
horizontal_beam_angles = theta_list
pendulum_angles = alpha_list

def project_point(p):
    x, y, z = p
    # Simple planar projection onto the screen
    return WIDTH // 2 + int(y), HEIGHT // 2 - int(z)


def draw_furuta_pendulum(screen, beam_angle, pendulum_angle):
    # Imagine the beam rotating around the vertical Z axis; calculate beam endpoints in 3D space
    beam_end = np.array([beam_length * np.cos(beam_angle), beam_length * np.sin(beam_angle), 0])

    # Project the end of the beam onto the screen
    beam_screen_x, beam_screen_y = project_point(beam_end)

    # Draw the beam (assuming it's a rod with negligible thickness in the Z-direction)
    pygame.draw.line(screen, BEAM_COLOR, (WIDTH // 2, HEIGHT // 2), (beam_screen_x, beam_screen_y), 5)

    # Calculate the pendulum endpoints in 3D space
    sp_m = rl.rotate_by_quaternion(sp, beam_angle, [0, 0, 1])
    pendulum_end = rl.rotate_by_quaternion(sp_m, pendulum_angle, [np.cos(beam_angle), np.sin(beam_angle), 0])


    # Project the end of the pendulum onto the screen
    pendulum_screen_x, pendulum_screen_y = project_point(pendulum_end)

    # Draw the pendulum line and ball (projected onto the screen)
    pygame.draw.line(screen, PENDULUM_COLOR, (beam_screen_x, beam_screen_y), (pendulum_screen_x, pendulum_screen_y), 2)
    # pygame.draw.circle(screen, PENDULUM_COLOR, (pendulum_screen_x, pendulum_screen_y), ball_radius)

def main():
    running = True
    frame_count = min(len(horizontal_beam_angles), len(pendulum_angles))

    for i in range(frame_count):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if not running:
            break

        screen.fill(BACKGROUND_COLOR)
        draw_furuta_pendulum(screen, horizontal_beam_angles[i], pendulum_angles[i])
        pygame.display.flip()

        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()