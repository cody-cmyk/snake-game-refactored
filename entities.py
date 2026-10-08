import turtle


class Snake:
    def __init__(self):
        self.segments = []

    def create_segment(self, is_head=False):
        segment = turtle.Turtle()
        segment.speed(0)
        segment.shape("circle")
        segment.penup()

        if is_head:
            segment.color("#00FF99")
            segment.shapesize(1.1, 1.1)
        else:
            segment.color("#73FBD3")
            segment.shapesize(1.0, 1.0)

        return segment

    def clear(self):
        for segment in self.segments:
            segment.hideturtle()
        self.segments.clear()

    def add_segment(self, segment):
        self.segments.append(segment)

    def __len__(self):
        return len(self.segments)

    def __iter__(self):
        return iter(self.segments)

    def head(self):
        if not self.segments:
            raise ValueError("Snake has no head segment.")
        return self.segments[0]

    def tail(self):
        if not self.segments:
            raise ValueError("Snake has no tail segment.")
        return self.segments[-1]


class Food:
    def __init__(self):
        self.turtle = turtle.Turtle()
        self.turtle.speed(0)
        self.turtle.shape("circle")
        self.turtle.color("#FF4D6D")
        self.turtle.penup()
        self.turtle.shapesize(0.8, 0.8)
        self.turtle.hideturtle()

    def show(self):
        self.turtle.showturtle()

    def hide(self):
        self.turtle.hideturtle()

    def goto(self, x, y):
        self.turtle.goto(x, y)

    def xcor(self):
        return self.turtle.xcor()

    def ycor(self):
        return self.turtle.ycor()

    def distance(self, other):
        return self.turtle.distance(other)


class BonusFood:
    def __init__(self):
        self.turtle = turtle.Turtle()
        self.turtle.speed(0)
        self.turtle.shape("triangle")
        self.turtle.color("#FFD166")
        self.turtle.penup()
        self.turtle.shapesize(0.8, 0.8)
        self.turtle.hideturtle()

    def show(self):
        self.turtle.showturtle()

    def hide(self):
        self.turtle.hideturtle()

    def goto(self, x, y):
        self.turtle.goto(x, y)

    def xcor(self):
        return self.turtle.xcor()

    def ycor(self):
        return self.turtle.ycor()

    def distance(self, other):
        return self.turtle.distance(other)
