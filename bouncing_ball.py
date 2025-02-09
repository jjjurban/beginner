import pygame
import pymunk
import pymunk.pygame_util
import math

# Constants
WIDTH, HEIGHT = 800, 600
BALL_RADIUS = 15
HEXAGON_RADIUS = 200
GRAVITY = (0, 900)
FRICTION = 0.8
REST = 0.8  # Restitution (bounciness)
ROTATION_SPEED = 0.001  # Adjusted rotation speed for even slower rotation

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True

# Initialize Pymunk Space
space = pymunk.Space()
space.gravity = GRAVITY
draw_options = pymunk.pygame_util.DrawOptions(screen)

# Create Ball
ball_body = pymunk.Body(1, pymunk.moment_for_circle(1, 0, BALL_RADIUS))
ball_body.position = (WIDTH // 2, HEIGHT // 4)
ball_shape = pymunk.Circle(ball_body, BALL_RADIUS)
ball_shape.elasticity = REST
ball_shape.friction = FRICTION
space.add(ball_body, ball_shape)

# Hexagon (Static Rotating Walls)
hexagon_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
hexagon_body.position = (WIDTH // 2, HEIGHT // 2)

def create_hexagon():
    """Creates the hexagon walls."""
    walls = []
    for i in range(6):
        angle1 = (math.pi / 3) * i
        angle2 = (math.pi / 3) * (i + 1)
        p1 = (HEXAGON_RADIUS * math.cos(angle1), HEXAGON_RADIUS * math.sin(angle1))
        p2 = (HEXAGON_RADIUS * math.cos(angle2), HEXAGON_RADIUS * math.sin(angle2))
        segment = pymunk.Segment(hexagon_body, p1, p2, 5)
        segment.elasticity = REST
        segment.friction = FRICTION
        walls.append(segment)
    return walls

hexagon_walls = create_hexagon()
space.add(hexagon_body, *hexagon_walls)  # ✅ Fix applied: Add body and shapes together

# Set a constant rotation speed
ROTATION_SPEED = 0.02  # Adjust as needed to get the desired rotation speed

# Main Game Loop
while running:
    screen.fill((30, 30, 30))

    # Apply constant rotation speed in one direction (no acceleration)
    hexagon_body.angle += ROTATION_SPEED  # This will rotate the hexagon at a fixed speed
    
    # Update the positions of the walls
    for wall in hexagon_walls:
        angle = hexagon_body.angle
        cos_a, sin_a = math.cos(angle), math.sin(angle)
        
        # Rotate the segment's endpoints
        p1_rot = (wall.a.x * cos_a - wall.a.y * sin_a, wall.a.x * sin_a + wall.a.y * cos_a)
        p2_rot = (wall.b.x * cos_a - wall.b.y * sin_a, wall.b.x * sin_a + wall.b.y * cos_a)
        
        # Remove the old wall and add the new one with the rotated position
        space.remove(wall)
        new_wall = pymunk.Segment(hexagon_body, p1_rot, p2_rot, 5)
        new_wall.elasticity = REST
        new_wall.friction = FRICTION
        space.add(new_wall)
        
        # Update the list with the new wall
        hexagon_walls[hexagon_walls.index(wall)] = new_wall

    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update Physics
    space.step(1/60)

    # Draw Everything
    space.debug_draw(draw_options)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
