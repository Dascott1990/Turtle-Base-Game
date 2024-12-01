import pygame
import random

# Initialize Pygame
pygame.init()

# --- Screen Setup ---
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Breakout Game")

# --- Colors ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# --- Paddle ---
paddle_width = 100
paddle_height = 15
paddle_speed = 15
paddle_y = screen_height - paddle_height - 10  # Fix paddle position near the bottom

# --- Ball ---
ball_radius = 10
ball_x = screen_width // 2
ball_y = screen_height // 2
ball_dx = 4
ball_dy = -4

# --- Bricks ---
brick_width = 60
brick_height = 20
bricks = []
brick_rows = 5
brick_columns = 10

# --- Score ---
score = 0
font = pygame.font.SysFont(None, 36)

# --- Functions ---

# Draw the paddle
def draw_paddle(x, y):
    pygame.draw.rect(screen, WHITE, (x, y, paddle_width, paddle_height))

# Draw the ball
def draw_ball(x, y):
    pygame.draw.circle(screen, RED, (x, y), ball_radius)

# Draw the bricks
def create_bricks():
    global bricks
    bricks = []
    for row in range(brick_rows):
        for col in range(brick_columns):
            brick_x = col * (brick_width + 10) + 50
            brick_y = row * (brick_height + 5) + 50
            bricks.append(pygame.Rect(brick_x, brick_y, brick_width, brick_height))

def draw_bricks():
    for brick in bricks:
        pygame.draw.rect(screen, BLUE, brick)

# Display score
def display_score():
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

# --- Game Loop ---
def game_loop():
    global paddle_x, ball_x, ball_y, ball_dx, ball_dy, score

    running = True
    clock = pygame.time.Clock()

    create_bricks()

    while running:
        screen.fill(BLACK)

        # Check for events (keyboard, quitting, mouse)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Get the mouse position for paddle movement
        mouse_x, _ = pygame.mouse.get_pos()  # Get the x-coordinate of the mouse
        paddle_x = mouse_x - paddle_width // 2  # Keep paddle centered with the mouse

        # Ensure the paddle stays within screen bounds
        if paddle_x < 0:
            paddle_x = 0
        if paddle_x > screen_width - paddle_width:
            paddle_x = screen_width - paddle_width

        # Update ball position
        ball_x += ball_dx
        ball_y += ball_dy

        # Ball collision with walls
        if ball_x <= 0 or ball_x >= screen_width:
            ball_dx *= -1
        if ball_y <= 0:
            ball_dy *= -1

        # Ball collision with paddle
        if paddle_y <= ball_y + ball_radius <= paddle_y + paddle_height and paddle_x <= ball_x <= paddle_x + paddle_width:
            ball_dy *= -1
            score += 10

        # Ball collision with bricks
        for brick in bricks:
            if brick.collidepoint(ball_x, ball_y):
                ball_dy *= -1
                bricks.remove(brick)
                score += 20
                break

        # Game Over condition
        if ball_y >= screen_height:
            running = False
            print("Game Over!")
            print(f"Final Score: {score}")

        # Draw everything
        draw_paddle(paddle_x, paddle_y)
        draw_ball(ball_x, ball_y)
        draw_bricks()
        display_score()

        # Display "PLAY" status (since we don't have a pause function in this version)
        play_text = font.render("PLAY", True, WHITE)
        screen.blit(play_text, (screen_width // 2 - 40, screen_height // 2 - 20))

        pygame.display.update()

        clock.tick(60)

    pygame.quit()

# --- Start the Game ---
game_loop()
