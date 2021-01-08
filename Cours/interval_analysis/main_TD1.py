import tkinter as tk
from interval.ifunctions import *
from TD1.work2do import evaluate_function, get_min_function, my_function

# domain for the drawing [x][y]
domain = [Interval(-3.05, 3.05), Interval(-3, 3)]

# list of boxes to enclose the function
listbox = []

# list of boxes to enclose the function minimum
listbox_min = []

# default values for the window size
width = 1
height = 3


# Main drawing function, it is called each time the window needs to be redraw
def draw():
    global drawing, domain, listbox, listbox_min
    drawing.delete("all")
    draw_list_box(listbox, 'green')
    draw_list_box(listbox_min, 'orange')
    draw_function(0.01, 'black')
    draw_axes()


# function to get the new size of the window
def resize_event(event):
    global width, height
    width = event.width
    height = event.height
    draw()


# to convert an X value from the world to the window frame
def real2draw_x(x):
    global domain, width
    step = width/(domain[0].sup-domain[0].inf)
    x_draw = (x-domain[0].inf)*step
    return x_draw


# to convert an Y value from the world to the window frame
def real2draw_y(y):
    global domain, height
    step = height/(domain[1].sup-domain[1].inf)
    y_draw = (y-domain[1].inf)*step
    return height-y_draw


# function to draw the function f(x)=x^2+2*x-exp(x)
def draw_function(step=1.0, color='black'):
    global domain
    x0 = domain[0].inf
    y0 = pow(x0, 2)+2*x0-exp(x0)
    while x0 < domain[0].sup:
        x1 = x0+step
        y1 = my_function(x1)
        drawing.create_line(real2draw_x(x0), real2draw_y(y0), real2draw_x(x1), real2draw_y(y1), fill=color)
        x0 = x1
        y0 = y1


# function to draw the origin axes
def draw_axes(color='grey'):
    global domain
    drawing.create_line(real2draw_x(domain[0].inf), real2draw_y(0), real2draw_x(domain[0].sup), real2draw_y(0),
                        fill=color)
    drawing.create_line(real2draw_x(0), real2draw_y(domain[1].inf), real2draw_x(0), real2draw_y(domain[1].sup),
                        fill=color)


# function to draw a list of boxes
def draw_list_box(list_of_boxes, color):
    for box in list_of_boxes:
        draw_box(box, color)


# function to draw a box
def draw_box(box, color):
    global drawing
    drawing.create_rectangle(real2draw_x(box[0].sup), real2draw_y(box[1].inf),
                             real2draw_x(box[0].inf), real2draw_y(box[1].sup), fill=color)


# creation of the window
window = tk.Tk()
window.title("TD1")  # define the name of the window
window.geometry("400x400+100+50")  # define the original size and position of the window
drawing = tk.Canvas(window, background='white')  # define the background color
drawing.pack(fill=tk.BOTH, expand=tk.YES, side=tk.TOP)
drawing.bind('<Configure>', resize_event)  # to get the resize event

# call of the function that find an enclosure of the function f
evaluate_function(listbox, 0.05, domain, my_function)

# call of the function that find an enclosure of the minimum of the function f
get_min_function(listbox_min, 0.04, domain, my_function)

# call of the loop to display the window
window.mainloop()
