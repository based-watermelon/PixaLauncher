from turtle import Turtle


class Ball(Turtle):

    def __init__(self):
        super().__init__()
        self.color("#f542f5")
        self.shape("circle")
        self.penup()
        self.x_move = 10
        self.y_move = 10
        self.move_speed = 1

    def move(self):
        new_x = self.xcor() + self.x_move
        new_y = self.ycor() + self.y_move
        self.goto(new_x, new_y)

    def bounce_y(self):
        self.y_move *= -1

    def bounce_x(self):
        # self.x_move *= -1
        # self.move_speed *= 1.5
        self.x_move *= -1

        # Speed increases after paddle bounce
        self.x_move *= 1.05
        self.y_move *= 1.05

    def reset_position(self):
        # self.goto(0, 0)
        # self.move_speed = 2
        # self.bounce_x()
        self.goto(0, 0)
        self.x_move = 10
        self.y_move = 10
        self.bounce_x()