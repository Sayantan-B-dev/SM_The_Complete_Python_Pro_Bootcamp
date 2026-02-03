from turtle import Turtle, Screen
import random

colors = ["red", "orange", "yellow", "green", "blue", "purple"]

screen = Screen()
screen.setup(width=500, height=400)

def create_turtles():
    turtles = []
    y_position = -100
    for color in colors:
        t = Turtle(shape="turtle")
        t.color(color)
        t.penup()
        t.goto(x=-230, y=y_position)
        y_position += 40
        turtles.append(t)
    return turtles

def get_bet():
    return screen.textinput(
        title="Make your bet",
        prompt=f"Enter a color from {colors}:"
    )

def ask_restart(title, winner):
    choice = screen.textinput(
        title=title,
        prompt=f"Winner is {winner}. Type 'restart' to play again."
    )
    return choice == "restart"

while True:
    screen.clear()
    screen.setup(width=500, height=400)

    user_bet = get_bet()
    if not user_bet:
        break

    all_turtles = create_turtles()
    is_race_on = True

    while is_race_on:
        for t in all_turtles:
            t.forward(random.randint(0, 10))
            if t.xcor() > 230:
                is_race_on = False
                winning_color = t.pencolor()

                if winning_color == user_bet:
                    restart = ask_restart("Winner", winning_color)
                else:
                    restart = ask_restart("Loser", winning_color)

                if restart:
                    break
                else:
                    screen.exitonclick()
                    exit()

screen.exitonclick()
