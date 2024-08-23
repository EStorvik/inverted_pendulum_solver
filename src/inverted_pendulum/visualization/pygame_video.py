import pygame
import robolie as rl
import sys
import numpy as np


def visualize_with_pygame(x, h, angle_z = 0, angle_y = 0):


    # Constants
    WIDTH, HEIGHT = 800, 600
    BACKGROUND_COLOR = (255, 255, 255)
    BEAM_COLOR = (0, 0, 255)
    BOX_COLOR = (0, 255, 0)
    PENDULUM_COLOR = (255, 0, 0)
    FPS = 60

    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    pygame.display.set_caption('Furuta Pendulum Simulation')

    # Pendulum settings
    beam_length = 250  # Length of the horizontal beam
    pendulum_length = 250  # Length of the pendulum
    ball_radius = 10  # Radius of the pendulum ball

    box_length =250
    # Define the box
    box = box_length * np.array(
        [
            [-0.5, -0.5, -1],
            [-0.5, -0.5, 0],
            [-0.5, 0.5, -1],
            [-0.5, 0.5, 0],
            [0.5, -0.5, -1],
            [0.5, -0.5, 0],
            [0.5, 0.5, -1],
            [0.5, 0.5, 0],
        ]
    )
    # Stationary point
    sp = np.array([beam_length, 0, -pendulum_length])

    # Sample data
    dx = int(1/(60*h))
    horizontal_beam_angles = x[0,slice(0, len(x[0,:]), dx)]
    pendulum_angles = x[2,slice(0, len(x[0,:]), dx)]
    print(len(horizontal_beam_angles))

    def project_point(p):
        p_l = rl.rotate_by_quaternion(p, angle_z, [0, 1, 0])
        p_l = rl.rotate_by_quaternion(p_l, angle_y, [0, 0, 1])
        x, y, z = p_l
        # Simple planar projection onto the screen
        return WIDTH // 2 + int(y), HEIGHT // 2 - int(z)


    def draw_base_box(screen):

        for edge in [
            (0, 1),
            (1, 3),
            (3, 2),
            (2, 0),
            (0, 4),
            (1, 5),
            (2, 6),
            (3, 7),
            (4, 5),
            (5, 7),
            (7, 6),
            (6, 4),
        ]:
            pygame.draw.line(
                screen,
                (0, 0, 0),
                (
                    project_point(box[edge[0]]),
                ),
                (
                    project_point(box[edge[1]]),
                ),
            )

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


    running = True
    frame_count = min(len(horizontal_beam_angles), len(pendulum_angles))
    
    for i in range(frame_count):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if not running:
            break
        
        screen.fill(BACKGROUND_COLOR)
        draw_base_box(screen)
        draw_furuta_pendulum(screen, horizontal_beam_angles[i], pendulum_angles[i])
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()
