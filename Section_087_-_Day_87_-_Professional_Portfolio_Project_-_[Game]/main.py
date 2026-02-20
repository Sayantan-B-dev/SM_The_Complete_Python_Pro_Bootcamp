import turtle          # Import the turtle graphics library for drawing shapes and handling user input
import time            # Import time module to add small delays for controlling game speed

# ---------------------------- SETUP ----------------------------
# Create the game window (screen)
screen = turtle.Screen()                     # Create a Screen object; this is the window where everything will be drawn
screen.title("Breakout")                      # Set the title of the window to "Breakout"
screen.bgcolor("black")                        # Set the background color of the window to black
screen.setup(width=800, height=600)            # Set the window size to 800 pixels wide and 600 pixels tall
screen.tracer(0)                               # Turn off automatic animation; we will manually update the screen for smoother control

# ---------------------------- CONSTANTS ----------------------------
# These are fixed values that we use throughout the game. Changing them here changes the game behavior.
PADDLE_WIDTH = 100      # Width of the paddle in pixels (5 * 20 because turtle's default square is 20x20, stretched 5 times)
PADDLE_HEIGHT = 20      # Height of the paddle (default square height 20, no stretch in height)
BALL_RADIUS = 10        # Radius of the ball (default circle has radius 10)
BRICK_WIDTH = 80        # Width of each brick (stretched from 20 to 80)
BRICK_HEIGHT = 30       # Height of each brick (stretched from 20 to 30)
BRICK_SPACING = 5       # Gap between bricks in pixels
BRICK_ROWS = 5          # Number of rows of bricks
BRICK_COLS = 8          # Number of columns of bricks
START_X = -350          # Starting x-coordinate for the leftmost brick (so bricks are centered)
START_Y = 200           # Starting y-coordinate for the top row of bricks

# Colors for each row (classic Breakout style: from top to bottom: red, orange, green, yellow, silver)
ROW_COLORS = ["red", "orange", "green", "yellow", "silver"]

# ---------------------------- GAME STATE ----------------------------
# These variables track the current status of the game.
game_active = False          # True when the ball is moving; False when it's waiting on the paddle
lives = 3                    # Number of lives remaining (player starts with 3)
score = 0                    # Player's current score
level = 1                    # Current level number (1 to 5)
game_over_flag = False       # Set to True when game is over (lost all lives) or player wins

# Paddle movement flags: these are set to True when the corresponding arrow key is pressed
left_pressed = False
right_pressed = False

# ---------------------------- CREATE GAME OBJECTS ----------------------------
# Create the paddle as a turtle object (a white square)
paddle = turtle.Turtle()                     # Create a new Turtle object for the paddle
paddle.shape("square")                        # Set its shape to a square
paddle.color("white")                          # Set its color to white
paddle.shapesize(stretch_wid=1, stretch_len=5) # Stretch the square: width 1 (20px), length 5 (100px) – this makes the paddle
paddle.penup()                                 # Lift the pen so it doesn't draw when moving
paddle.goto(0, -250)                           # Position the paddle near the bottom of the screen (x=0, y=-250)

# Create the ball as a turtle object (a white circle)
ball = turtle.Turtle()                         # Create a new Turtle object for the ball
ball.shape("circle")                            # Set its shape to a circle
ball.color("white")                              # Set its color to white
ball.penup()                                     # Lift the pen
ball.goto(0, -230)                               # Start the ball just above the paddle (y = paddle's y + 20? Actually paddle at -250, ball at -230, so 20 pixels above)
ball.dx = 3   # horizontal speed (change in x per frame) – positive means moving right
ball.dy = 3   # vertical speed (change in y per frame) – positive means moving up

bricks = []   # Create an empty list that will hold all the brick objects

# ---------------------------- UI ELEMENTS ----------------------------
# Create turtle objects to display score, lives, level, and messages on the screen
score_display = turtle.Turtle()                # Create a turtle for score
score_display.color("white")                    # Set text color
score_display.penup()                            # No drawing while moving
score_display.hideturtle()                       # Hide the turtle icon (we only want the text)
score_display.goto(300, 260)                     # Position it near the top-right corner

lives_display = turtle.Turtle()                  # Turtle for lives
lives_display.color("white")
lives_display.penup()
lives_display.hideturtle()
lives_display.goto(-300, 260)                    # Top-left corner

level_display = turtle.Turtle()                  # Turtle for level
level_display.color("white")
level_display.penup()
level_display.hideturtle()
level_display.goto(0, 260)                        # Top-center

message_display = turtle.Turtle()                 # Turtle for showing messages like "Game Over"
message_display.color("white")
message_display.penup()
message_display.hideturtle()

def update_ui():
    """Refresh the score, lives, and level numbers on the screen."""
    score_display.clear()                         # Erase previous score text
    score_display.write(f"Score: {score}", align="center", font=("Courier", 16, "normal"))
    lives_display.clear()                          # Erase previous lives text
    lives_display.write(f"Lives: {lives}", align="center", font=("Courier", 16, "normal"))
    level_display.clear()                          # Erase previous level text
    level_display.write(f"Level: {level}", align="center", font=("Courier", 16, "normal"))

def show_message(text):
    """Display a centered message on the screen (e.g., 'Game Over')."""
    message_display.clear()                        # Remove any previous message
    message_display.goto(0, 0)                     # Move to the center of the screen
    message_display.write(text, align="center", font=("Courier", 24, "normal"))

def hide_message():
    """Clear the message from the screen."""
    message_display.clear()

# ---------------------------- BRICK MANAGEMENT ----------------------------
def create_bricks():
    """Create a grid of bricks with different colors per row."""
    for row in range(BRICK_ROWS):                  # Loop over each row (0 to 4)
        color = ROW_COLORS[row % len(ROW_COLORS)]  # Pick color from list (repeats if more rows than colors)
        for col in range(BRICK_COLS):              # Loop over each column (0 to 7)
            brick = turtle.Turtle()                 # Create a new turtle for the brick
            brick.shape("square")                    # Shape is square
            brick.color(color)                        # Set its color
            brick.shapesize(stretch_wid=BRICK_HEIGHT/20, stretch_len=BRICK_WIDTH/20)  # Stretch to brick size (since default is 20x20)
            brick.penup()                              # Lift pen
            # Calculate x and y position based on row and column
            x = START_X + col * (BRICK_WIDTH + BRICK_SPACING)  # x = leftmost start + column * (brick width + gap)
            y = START_Y - row * (BRICK_HEIGHT + BRICK_SPACING) # y = top start - row * (brick height + gap) (negative because going down)
            brick.goto(x, y)                           # Place the brick
            bricks.append(brick)                       # Add brick to the bricks list

def clear_bricks():
    """Remove all bricks from the screen and empty the list."""
    for brick in bricks:               # Loop through all bricks
        brick.hideturtle()               # Hide each brick (makes it disappear)
    bricks.clear()                       # Clear the list (remove references)

# ---------------------------- GAME CONTROL FUNCTIONS ----------------------------
def reset_ball():
    """Place the ball back on the paddle and stop its movement."""
    ball.goto(paddle.xcor(), paddle.ycor() + 30)   # Position ball above paddle (30 pixels up)
    # Increase speed slightly with each level (base speed 3, add 0.5 per level)
    base_speed = 3 + (level - 1) * 0.5
    ball.dx = base_speed                             # Set horizontal speed
    ball.dy = base_speed                             # Set vertical speed

def serve_ball():
    """Launch the ball from the paddle when the game is ready."""
    global game_active, game_over_flag                # We need to modify these global variables
    if not game_active and not game_over_flag:       # If game is not active and not over/won
        game_active = True                             # Start the ball moving
        hide_message()                                  # Remove any message from the screen

def next_level():
    """Advance to the next level after all bricks are cleared."""
    global level, game_active                          # Modify global level and game_active
    level += 1                                          # Increase level by 1
    if level > 5:                                       # If we passed level 5, player wins
        win_game()
    else:
        clear_bricks()                                  # Remove old bricks
        create_bricks()                                 # Create new bricks for next level
        reset_ball()                                    # Put ball back on paddle
        game_active = False                              # Wait for player to press space
        show_message(f"Level {level} - Press SPACE")    # Show level start message
        update_ui()                                      # Update level display

def game_over():
    """Handle game over when lives reach zero."""
    global game_active, game_over_flag
    game_active = False
    game_over_flag = True                               # Mark game as over
    show_message("GAME OVER - Press R to restart")

def win_game():
    """Handle winning condition (after level 5)."""
    global game_active, game_over_flag
    game_active = False
    game_over_flag = True                               # Game ends (win is still a kind of over)
    show_message("YOU WIN! Press R to restart")

def restart_game():
    """Reset everything to start a new game from level 1."""
    global lives, score, level, game_active, game_over_flag
    lives = 3
    score = 0
    level = 1
    game_active = False
    game_over_flag = False

    clear_bricks()                                       # Remove any existing bricks
    create_bricks()                                      # Create fresh bricks for level 1
    paddle.goto(0, -250)                                 # Reset paddle position
    reset_ball()                                          # Place ball on paddle
    update_ui()                                           # Update score/lives/level displays
    hide_message()                                        # Clear any messages

# ---------------------------- PADDLE MOVEMENT (SMOOTH) ----------------------------
# These functions are called when arrow keys are pressed or released.
def start_move_left():
    global left_pressed
    left_pressed = True

def stop_move_left():
    global left_pressed
    left_pressed = False

def start_move_right():
    global right_pressed
    right_pressed = True

def stop_move_right():
    global right_pressed
    right_pressed = False

# Keyboard bindings: tell the screen to call these functions when keys are used
screen.listen()                                         # Make the screen listen for key presses
screen.onkeypress(start_move_left, "Left")              # When Left arrow is pressed, call start_move_left
screen.onkeyrelease(stop_move_left, "Left")             # When Left arrow is released, call stop_move_left
screen.onkeypress(start_move_right, "Right")
screen.onkeyrelease(stop_move_right, "Right")
screen.onkeypress(serve_ball, "space")                  # When Space is pressed, call serve_ball
screen.onkeypress(restart_game, "r")                    # When 'r' is pressed, call restart_game

# Initial bricks and UI setup
create_bricks()                                          # Build the brick wall
update_ui()                                              # Show initial score, lives, level
show_message("Level 1 - Press SPACE")                    # Prompt player to start

# ---------------------------- MAIN GAME LOOP ----------------------------
# This loop runs forever, updating the game state and redrawing.
while True:
    screen.update()                                      # Manually update the screen (because tracer is off)
    time.sleep(0.01)                                     # Small delay to control game speed (about 100 FPS)

    # If the game is over or won, skip all game logic except listening for 'R' (already bound)
    if game_over_flag:
        continue                                          # Go to next iteration of loop

    # Smooth paddle movement based on which keys are currently held down
    if left_pressed:
        new_x = paddle.xcor() - 10                        # Move left by 10 pixels
        # Check if paddle would go beyond left boundary (with its half-width)
        if new_x > -350 + PADDLE_WIDTH/2:
            paddle.setx(new_x)                             # Update paddle's x position
    if right_pressed:
        new_x = paddle.xcor() + 10                         # Move right by 10 pixels
        if new_x < 350 - PADDLE_WIDTH/2:
            paddle.setx(new_x)

    # If game is not active (ball waiting), keep ball on paddle
    if not game_active:
        ball.goto(paddle.xcor(), paddle.ycor() + 30)       # Stick ball to paddle
        continue                                            # Skip the rest of the loop

    # Move the ball by adding its speed to its coordinates
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    # Wall collisions (top, left, right)
    if ball.ycor() > 290:                                  # If ball hits top wall (y > 290, since screen top is 300, ball radius 10)
        ball.sety(290)                                      # Place it exactly at the collision boundary
        ball.dy *= -1                                       # Reverse vertical direction (bounce)

    if ball.xcor() > 390:                                   # Right wall (x > 390, since screen right is 400, radius 10)
        ball.setx(390)
        ball.dx *= -1
    elif ball.xcor() < -390:                                # Left wall
        ball.setx(-390)
        ball.dx *= -1

    # Bottom wall: ball falls below screen (y < -290) – lose a life
    if ball.ycor() < -290:
        lives -= 1                                           # Decrease lives by 1
        update_ui()                                          # Update lives display
        if lives > 0:                                        # If player still has lives
            game_active = False                               # Stop ball movement
            reset_ball()                                      # Place ball back on paddle
            show_message(f"Lives left: {lives} - Press SPACE") # Prompt to continue
        else:
            game_over()                                       # No lives left, game over
            continue                                          # Skip rest of loop (won't process bricks)

    # Paddle collision detection
    # Check if ball's bottom edge is below paddle's top edge and ball's x is within paddle's horizontal range
    if (ball.ycor() - BALL_RADIUS < paddle.ycor() + PADDLE_HEIGHT/2 and
        ball.xcor() > paddle.xcor() - PADDLE_WIDTH/2 and
        ball.xcor() < paddle.xcor() + PADDLE_WIDTH/2):
        # Move ball just above paddle to prevent sticking
        ball.sety(paddle.ycor() + PADDLE_HEIGHT/2 + BALL_RADIUS)
        ball.dy *= -1                                        # Reverse vertical direction (bounce up)
        # Optional spin effect (commented out to keep simple)
        # offset = ball.xcor() - paddle.xcor()
        # ball.dx += offset * 0.1
        # Clamp speed to avoid going too fast
        if abs(ball.dx) > 8:
            ball.dx = 8 if ball.dx > 0 else -8
        if abs(ball.dy) > 8:
            ball.dy = 8 if ball.dy > 0 else -8

    # Brick collisions – iterate over a copy of the bricks list because we might remove bricks
    for brick in bricks[:]:   # Using [:] creates a copy, so we can safely remove from original list while looping
        # Calculate brick's edges
        brick_left = brick.xcor() - BRICK_WIDTH/2
        brick_right = brick.xcor() + BRICK_WIDTH/2
        brick_bottom = brick.ycor() - BRICK_HEIGHT/2
        brick_top = brick.ycor() + BRICK_HEIGHT/2

        # Check if ball overlaps with brick (simple axis-aligned bounding box collision)
        if (ball.xcor() + BALL_RADIUS > brick_left and
            ball.xcor() - BALL_RADIUS < brick_right and
            ball.ycor() + BALL_RADIUS > brick_bottom and
            ball.ycor() - BALL_RADIUS < brick_top):

            # Remove the brick
            brick.hideturtle()            # Make it disappear
            bricks.remove(brick)           # Remove from bricks list

            # Increase score
            score += 10
            update_ui()

            # Determine which side of the brick the ball hit to decide bounce direction
            # Calculate distance from ball to brick center
            dx = ball.xcor() - brick.xcor()
            dy = ball.ycor() - brick.ycor()

            # Compute overlap amounts
            overlap_x = BRICK_WIDTH/2 + BALL_RADIUS - abs(dx)
            overlap_y = BRICK_HEIGHT/2 + BALL_RADIUS - abs(dy)

            # If overlap in y is smaller than overlap in x, it's a vertical collision (top/bottom)
            if overlap_x > overlap_y:
                ball.dy *= -1                      # Reverse vertical direction
                # Push ball out of brick to avoid multiple collisions in same frame
                if dy > 0:
                    ball.sety(brick_top + BALL_RADIUS)   # Ball above brick
                else:
                    ball.sety(brick_bottom - BALL_RADIUS) # Ball below brick
            else:
                ball.dx *= -1                      # Reverse horizontal direction
                if dx > 0:
                    ball.setx(brick_right + BALL_RADIUS)  # Ball to the right of brick
                else:
                    ball.setx(brick_left - BALL_RADIUS)   # Ball to the left of brick

            break  # Only handle one brick per frame to avoid double-bouncing

    # Check if all bricks are destroyed – if so, go to next level
    if len(bricks) == 0:
        next_level()