import pygame
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Breakout')

# Set up the clock for controlling the frame rate
clock = pygame.time.Clock()

# Paddle properties
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 20
paddle_x = (SCREEN_WIDTH - PADDLE_WIDTH) // 2
paddle_y = SCREEN_HEIGHT - 30
paddle_speed = 10

# Ball properties
BALL_SIZE = 20
ball_x = SCREEN_WIDTH // 2
ball_y = SCREEN_HEIGHT // 2
ball_speed_x = 5
ball_speed_y = -5

# Brick properties
BRICK_ROWS = 5
BRICK_COLS = 10
BRICK_WIDTH = SCREEN_WIDTH // BRICK_COLS
BRICK_HEIGHT = 30

# Create a list to store bricks
bricks = []
for row in range(BRICK_ROWS):
    for col in range(BRICK_COLS):
        brick_x = col * BRICK_WIDTH
        brick_y = row * BRICK_HEIGHT
        bricks.append(pygame.Rect(brick_x, brick_y, BRICK_WIDTH, BRICK_HEIGHT))

# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle paddle movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        paddle_x -= paddle_speed
    if keys[pygame.K_RIGHT]:
        paddle_x += paddle_speed

    # Prevent the paddle from moving out of bounds
    if paddle_x < 0:
        paddle_x = 0
    if paddle_x > SCREEN_WIDTH - PADDLE_WIDTH:
        paddle_x = SCREEN_WIDTH - PADDLE_WIDTH

    # Move the ball
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # Ball collision with walls
    if ball_x <= 0 or ball_x >= SCREEN_WIDTH - BALL_SIZE:
        ball_speed_x = -ball_speed_x
    if ball_y <= 0:
        ball_speed_y = -ball_speed_y

    # Ball collision with paddle
    if (paddle_y <= ball_y + BALL_SIZE <= paddle_y + PADDLE_HEIGHT and
            paddle_x <= ball_x <= paddle_x + PADDLE_WIDTH):
        ball_speed_y = -ball_speed_y

    # Ball collision with bricks
    ball_rect = pygame.Rect(ball_x, ball_y, BALL_SIZE, BALL_SIZE)
    hit_index = ball_rect.collidelist(bricks)
    if hit_index != -1:
        hit_rect = bricks.pop(hit_index)
        ball_speed_y = -ball_speed_y

    # Ball falls below the paddle (lose condition)
    if ball_y > SCREEN_HEIGHT:
        print("You lose!")
        running = False

    # Check for win condition
    if not bricks:
        print("You win!")
        running = False

    # Clear the screen
    screen.fill(BLACK)

    # Draw the paddle
    pygame.draw.rect(screen, WHITE, (paddle_x, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT))

    # Draw the ball
    pygame.draw.ellipse(screen, RED, (ball_x, ball_y, BALL_SIZE, BALL_SIZE))

    # Draw the bricks
    for brick in bricks:
        pygame.draw.rect(screen, BLUE, brick)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Clean up
pygame.quit()
sys.exit()
