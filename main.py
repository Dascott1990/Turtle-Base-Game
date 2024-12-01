import turtle
import random
import time

# --- Screen Setup ---
screen = turtle.Screen()
screen.title("Breakout Game")
screen.bgcolor("black")
screen.setup(width=800, height=600)
screen.tracer(0)  # Disable automatic screen updates

# --- Paddle ---
paddle = turtle.Turtle()
paddle.shape("square")
paddle.color("white")
paddle.shapesize(stretch_wid=1, stretch_len=5)
paddle.penup()
paddle.goto(0, -250)

# --- Ball ---
ball = turtle.Turtle()
ball.shape("circle")
ball.color("red")
ball.penup()
ball.goto(0, -200)
ball.dx = 3
ball.dy = 3

# --- Score Display ---
score_display = turtle.Turtle()
score_display.color("white")
score_display.penup()
score_display.hideturtle()
score_display.goto(0, 260)

# --- Lives Display ---
lives_display = turtle.Turtle()
lives_display.color("white")
lives_display.penup()
lives_display.hideturtle()
lives_display.goto(-350, 260)

# --- Bricks ---
bricks = []

def create_bricks(rows, columns):
    """Create bricks in a grid."""
    x_start, y_start = -350, 250
    for row in range(rows):
        for col in range(columns):
            brick = turtle.Turtle()
            brick.shape("square")
            brick.color(random.choice(["blue", "green", "yellow", "purple"]))
            brick.shapesize(stretch_wid=1, stretch_len=2)
            brick.penup()
            brick.goto(x_start + col * 80, y_start - row * 30)
            bricks.append(brick)

# --- Paddle Movement ---
def move_left():
    x = paddle.xcor() - 20
    if x > -360:
        paddle.setx(x)

def move_right():
    x = paddle.xcor() + 20
    if x < 360:
        paddle.setx(x)

screen.listen()
screen.onkeypress(move_left, "Left")
screen.onkeypress(move_right, "Right")

# --- Game Variables ---
game_paused = False
total_score = 0
lives = 3

# --- Update Score and Lives ---
def update_score_and_lives():
    score_display.clear()
    score_display.write(f"Score: {total_score}", align="center", font=("Courier", 24, "normal"))
    lives_display.clear()
    lives_display.write(f"Lives: {lives}", align="center", font=("Courier", 24, "normal"))

# --- Play a Single Round ---
def play_round(level):
    global total_score, lives, ball, bricks

    # Level configurations
    rows, columns = level + 2, 7 + level
    ball.dx, ball.dy = 3 + level, 3 + level

    # Reset bricks and ball
    for brick in bricks:
        brick.hideturtle()
    bricks.clear()
    create_bricks(rows, columns)
    ball.goto(0, -200)
    ball.dx = random.choice([-ball.dx, ball.dx])
    ball.dy = abs(ball.dy)

    # Main game loop
    game_on = True
    while game_on:
        screen.update()
        if not game_paused:
            ball.setx(ball.xcor() + ball.dx)
            ball.sety(ball.ycor() + ball.dy)

            # Ball collision with walls
            if ball.xcor() > 390 or ball.xcor() < -390:
                ball.dx *= -1
            if ball.ycor() > 290:
                ball.dy *= -1

            # Ball collision with paddle
            if (ball.ycor() < -240 and paddle.xcor() - 50 < ball.xcor() < paddle.xcor() + 50):
                ball.dy *= -1

            # Ball collision with bricks
            for brick in bricks[:]:
                if brick.distance(ball) < 25:
                    brick.hideturtle()  # Hide brick when hit
                    bricks.remove(brick)
                    total_score += 10
                    update_score_and_lives()
                    ball.dy *= -1
                    break  # Break to prevent multiple collisions

            # Game Over Conditions
            if ball.ycor() < -290:
                lives -= 1
                update_score_and_lives()
                if lives == 0:
                    game_on = False
                else:
                    ball.goto(0, -200)
                    ball.dx = random.choice([-ball.dx, ball.dx])
                    ball.dy = abs(ball.dy)

            if not bricks:
                game_on = False

# --- Main Game ---
def play_game():
    global total_score, lives
    total_score = 0
    lives = 3
    update_score_and_lives()

    # Game Intro
    score_display.clear()
    score_display.write("Press 'Left' or 'Right' to Move the Paddle", align="center", font=("Courier", 18, "normal"))
    time.sleep(2)

    for level in range(1, 4):  # Three levels
        score_display.clear()
        score_display.write(f"Level {level} Start!", align="center", font=("Courier", 24, "normal"))
        time.sleep(2)
        play_round(level)
        if lives == 0:
            break

    # Game Over Screen
    score_display.clear()
    score_display.write(f"Game Over! Final Score: {total_score}\nPress 'R' to Restart",
                        align="center", font=("Courier", 24, "normal"))

# --- Restart Game ---
def restart_game():
    global total_score, lives, bricks
    total_score = 0
    lives = 3
    bricks.clear()
    play_game()

screen.onkeypress(restart_game, "r")

# --- Start Game ---
play_game()

# Keep screen open
screen.mainloop()
