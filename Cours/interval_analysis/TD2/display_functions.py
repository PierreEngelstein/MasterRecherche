import TD2.global_variables as gv

"""You do not need to modify this file"""


# to convert an X value from the world to the window frame
def real2draw_x(x):
    step = gv.WIDTH/(gv.DOMAIN[0].sup-gv.DOMAIN[0].inf)
    x_draw = (x-gv.DOMAIN[0].inf)*step
    return x_draw


# to convert an Y value from the world to the window frame
def real2draw_y(y):
    step = gv.HEIGHT/(gv.DOMAIN[1].sup-gv.DOMAIN[1].inf)
    y_draw = (y-gv.DOMAIN[1].inf)*step
    return gv.HEIGHT-y_draw


# to convert an X value from the window frame to the world
def draw2real_x(x):
    step = abs(gv.DOMAIN[0].sup-gv.DOMAIN[0].inf)/float(gv.WIDTH)
    x_real = x*step+gv.DOMAIN[0].inf
    return x_real


# to convert an Y value from the world to the window frame
def draw2real_y(y):
    step = abs(gv.DOMAIN[1].sup-gv.DOMAIN[1].inf)/float(gv.HEIGHT)
    y_real = (gv.HEIGHT-y)*step+gv.DOMAIN[1].inf
    return y_real


# to get the pointed coordinates of the window
def mouse(event):
    gv.xMOUSE = draw2real_x(event.x)
    gv.yMOUSE = draw2real_y(event.y)
    draw()


# function to draw the origin axes
def draw_axes(step=1.0, color='grey'):
    i = gv.DOMAIN[0].inf
    while i < gv.DOMAIN[0].sup+step:
        gv.DRAWING.create_line(real2draw_x(i), real2draw_y(gv.DOMAIN[1].inf), real2draw_x(i),
                               real2draw_y(gv.DOMAIN[1].sup), fill=color)
        i = i+step
    i = gv.DOMAIN[1].inf
    while i < gv.DOMAIN[1].sup+step:
        gv.DRAWING.create_line(real2draw_x(gv.DOMAIN[0].inf), real2draw_y(i), real2draw_x(gv.DOMAIN[0].sup),
                               real2draw_y(i), fill=color)
        i = i+step


# function to get the new size of the window
def resize_event(event):
    gv.WIDTH = event.width
    gv.HEIGHT = event.height
    draw()


def draw_box(box, color='white'):
    x1 = real2draw_x(box[0].sup)
    y1 = real2draw_y(box[1].inf)
    x2 = real2draw_x(box[0].inf)
    y2 = real2draw_y(box[1].sup)
    if x1 < 0:
        x1 = 0
    if y1 < 0:
        y1 = 0
    if x2 < 0:
        x2 = 0
    if y2 < 0:
        y2 = 0
    gv.DRAWING.create_rectangle(x1, y1, x2, y2, fill=color, outline='black', width=2)


# function to draw a list of IPose
def draw_boxes(boxes, color='white'):
    for box in boxes:
        draw_box(box, color)


# Main drawing function, it is called each time the window needs to be redraw
def draw():
    gv.DRAWING.delete("all")
    draw_boxes(gv.RED, "red")
    draw_boxes(gv.BLUE, "blue")
    draw_boxes(gv.YELLOW, "yellow")
    draw_axes(1)
