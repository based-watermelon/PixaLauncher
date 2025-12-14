from turtle import Screen,Turtle
from paddle import Paddle
from ball import Ball
from scoreboard import Scoreboard
import time


screen = Screen()
screen.bgcolor("#111")
screen.setup(width=800, height=600)
screen.title("Pong")
screen.tracer(0)

r_paddle = Paddle((350, 0))
l_paddle = Paddle((-350, 0))
ball = Ball()
scoreboard = Scoreboard()
'''
t = Turtle()
t.speed(0)

radius = 80

# Move to left edge of the circle
t.penup()
t.pencolor("white")
t.goto(0, -radius)   # Start at bottom so the circle is centered
t.pendown()

# Draw the circle
t.circle(radius)
t.hideturtle()
'''

t = Turtle()
t.speed(0)

radius = 90
num_dashes = 30          # number of dashes around the circle
step_angle = 360 / num_dashes

# Move to bottom of circle
t.penup()
t.goto(0, -radius)
t.setheading(0)
t.hideturtle()

# Draw dashed circle
for _ in range(num_dashes):
    t.pencolor('white')
    t.pendown()
    t.circle(radius, step_angle / 2)   # draw half the segment
    t.penup()
    t.circle(radius, step_angle / 2)

# this is to draw the center dotted line
dash = Turtle()
dash.color("white")
dash.hideturtle()
dash.penup()
dash.goto(0, 300)
dash.setheading(270)

for _ in range(25):
    dash.pendown()
    dash.forward(20)
    dash.penup()
    dash.forward(20)

# this is to make the paddles move
screen.listen()
screen.onkey(r_paddle.go_up, "Up")
screen.onkey(r_paddle.go_down, "Down")
screen.onkey(l_paddle.go_up, "w")
screen.onkey(l_paddle.go_down, "s")

game_is_on = True
while game_is_on:
    time.sleep(0.05) 
    screen.update()
    ball.move()

    #Detect collision with wall
    if ball.ycor() > 280 or ball.ycor() < -280:
        ball.bounce_y()

    #Detect collision with paddle
    if ball.distance(r_paddle) < 55 and ball.xcor() > 320 or ball.distance(l_paddle) < 55 and ball.xcor() < -320:
        ball.bounce_x()

    #Detect R paddle misses
    if ball.xcor() > 380:
        ball.reset_position()
        scoreboard.l_point()

    #Detect L paddle misses:
    if ball.xcor() < -380:
        ball.reset_position()
        scoreboard.r_point()
    

screen.exitonclick()