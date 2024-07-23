import turtle # turtle graphics

s = turtle.getscreen() # gets the screen

t = turtle.Turtle() # starts at right:

size = t.turtlesize() # default size is 1
increase = (2 * num for num in size) # double the size
t.turtlesize(*increase) # set the size to double

t.pensize(5) # set the pen size to 5
t.shapesize() # get the size of the turtle
t.pencolor("blue")

def go_right():
    # target = 0
    current = t.heading()
    if current == 0:
        pass
    elif current == 90:
        t.right(90)
    elif current == 180:
        t.right(180)
    elif current == 270:
        t.left(90)
    else:
        raise ValueError('not a right angle!')

def go_up():
    # target = 90
    current = t.heading()
    if current == 0:
        t.left(90)
    elif current == 90:
        pass
    elif current == 180:
        t.right(90)
    elif current == 270:
        t.left(180)
    else:
        raise ValueError('not a right angle!')
    
def go_left():
    # target = 180
    current = t.heading()
    if current == 0:
        t.left(180)
    elif current == 90:
        t.left(90)
    elif current == 180:
        pass
    elif current == 270:
        t.right(90)
    else:
        raise ValueError('not a right angle!')
    
def go_down():
    # target = 270
    current = t.heading()
    if current == 0:
        t.right(90)
    elif current == 90:
        t.right(180)
    elif current == 180:
        t.left(90)
    elif current == 270:
        pass
    else:
        raise ValueError('not a right angle!')


def move_turtle(command):
    if command == 'quay lên trên':
        go_up()
    elif command == 'quay xuống dưới':
        go_down()
    elif command == 'quay sang trái':
        go_left()
    elif command == 'quay sang phải':
        go_right()
    elif command == 'tiến lên':
        t.forward(100) # 
    elif command == 'dừng lại':
        print('Dừng Turtle.')
