import pygame
import math

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
SHADOW_COLOR = (50, 50, 50)  # Dark gray for the shadow

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

# Load brick image
brick_image = pygame.image.load("static/bricks.jpeg")

# --- Score ---
score = 0
font = pygame.font.SysFont(None, 36)

# Animation time variable
animation_time = 0


# --- Functions ---

# Draw the paddle
def draw_paddle(x, y):
    pygame.draw.rect(screen, WHITE, (x, y, paddle_width, paddle_height))


# Draw the ball
def draw_ball(x, y):
    pygame.draw.circle(screen, RED, (x, y), ball_radius)


# Create the bricks
def create_bricks():
    global bricks
    bricks = []
    for row in range(brick_rows):
        for col in range(brick_columns):
            brick_x = col * (brick_width + 10) + 50
            brick_y = row * (brick_height + 5) + 50
            bricks.append(pygame.Rect(brick_x, brick_y, brick_width, brick_height))


# Draw the bricks with shadow and breathing effect
def draw_bricks():
    global animation_time
    animation_time += 1  # Increment time for the breathing animation

    for brick in bricks:
        # Shadow Effect
        shadow_rect = pygame.Rect(
            brick.x + 5, brick.y + 5, brick_width, brick_height
        )  # Offset shadow
        pygame.draw.rect(screen, SHADOW_COLOR, shadow_rect, border_radius=5)

        # Breathing Effect
        scale_factor = 1 + 0.1 * math.sin(animation_time / 20)  # Smooth scaling
        scaled_width = int(brick_width * scale_factor)
        scaled_height = int(brick_height * scale_factor)
        scaled_image = pygame.transform.scale(brick_image, (scaled_width, scaled_height))

        # Center scaled image on the original brick position
        x_offset = (scaled_width - brick_width) // 2
        y_offset = (scaled_height - brick_height) // 2
        screen.blit(scaled_image, (brick.x - x_offset, brick.y - y_offset))


# Display score
def display_score():
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))


# Display "Game Over"
def display_game_over():
    game_over_font = pygame.font.SysFont(None, 72)
    score_font = pygame.font.SysFont(None, 36)
    game_over_text = game_over_font.render("GAME OVER", True, RED)
    score_text = score_font.render(f"Final Score: {score}", True, WHITE)

    screen.blit(game_over_text,
                (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 2 - game_over_text.get_height()))
    screen.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, screen_height // 2 + 50))
    pygame.display.update()
    pygame.time.delay(3000)  # Pause for 3 seconds to show the message


# Display "Paused"
def display_paused():
    paused_font = pygame.font.SysFont(None, 72)
    paused_text = paused_font.render("PAUSED", True, WHITE)
    screen.blit(paused_text,
                (screen_width // 2 - paused_text.get_width() // 2, screen_height // 2 - paused_text.get_height() // 2))
    pygame.display.update()


# --- Game Loop ---
def game_loop():
    global paddle_x, ball_x, ball_y, ball_dx, ball_dy, score

    running = True
    paused = False
    clock = pygame.time.Clock()

    create_bricks()

    while running:
        screen.fill(BLACK)

        # Check for events (keyboard, quitting, mouse)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # Pause/Play toggle
                    paused = not paused

        # If the game is paused, display "Paused" and skip the rest of the loop
        if paused:
            display_score()  # Display the score during the pause
            display_paused()
            clock.tick(30)  # Reduce FPS when paused
            continue

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
            display_game_over()
            running = False

        # Draw everything
        draw_paddle(paddle_x, paddle_y)
        draw_ball(ball_x, ball_y)
        draw_bricks()
        display_score()

        pygame.display.update()
        clock.tick(60)

    pygame.quit()


# --- Start the Game ---
game_loop()
