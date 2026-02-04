import turtle

# SCREEN SETUP
screen = turtle.Screen()
screen.title("Etch-A-Sketch — Turtle Event System")
screen.setup(width=700, height=700)

# TURTLE SETUP
pen = turtle.Turtle()
pen.shape("classic")
pen.speed(0)        # Fastest drawing speed
pen.pensize(2)      # Visible line thickness
pen.setheading(90)

# MOVEMENT FUNCTIONS

def move_forward():
    """
    Moves the turtle forward in the direction
    it is currently facing.
    """
    pen.forward(20)

def move_backward():
    pen.backward(20)

def turn_left():
    """
    Rotates turtle counter-clockwise
    without changing position.
    """
    pen.left(15)

def turn_right():
    pen.right(15)

def clear_screen():
    """
    Clears drawing and resets turtle
    to center with default orientation.
    """
    pen.speed(2)
    pen.clear()
    pen.penup()
    pen.home()
    pen.pendown()
    pen.setheading(90)
    pen.speed(0)

# EVENT LISTENERS
screen.listen()

# Keyboard bindings (higher-order usage)
screen.onkey(move_forward, "w")
screen.onkey(move_backward, "s")
screen.onkey(turn_left, "a")
screen.onkey(turn_right, "d")
screen.onkey(move_forward, "Up")
screen.onkey(move_backward, "Down")
screen.onkey(turn_left, "Left")
screen.onkey(turn_right, "Right")
screen.onkey(clear_screen, "c")

# EVENT LOOP
screen.mainloop()
