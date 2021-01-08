import TD6.global_variables as gv
from math import cos, sin

"""
    File that contains all the functions needed to display the simulation using Tkinter
    
    You do not need to modify this file

    This file needs the following global variables:
        WIDTH : the saved 'width' size of the window
        HEIGHT : the saved 'height' size of the window
        WORLD_X, WORLD_Y :  the box corresponding to the bounded environment
        ROBOT : the robot
        SENSOR : the robot's sensor (that includes the landmarks)
        DRAWING : the Tkinter canvas where we draw
        I_LANDMARKS : the known position of the landmarks ([x],[y])
        I_POSE : the known pose of the robot ([x],[y], [theta])
"""


def real2draw_x(x):
    """
        Function to convert an x value from the world to the window frame
        :param x : x value of the world
        :return x_draw : corresponding value in the window frame
    """
    step = float(gv.WIDTH) / (gv.WORLD_X.sup - gv.WORLD_X.inf)
    x_draw = (x - gv.WORLD_X.inf) * step
    return x_draw


def real2draw_y(y):
    """
        Function to convert an y value from the world to the window frame
        :param y : y value of the world
        :return y_draw : corresponding value in the window frame
    """
    step = float(gv.HEIGHT) / (gv.WORLD_Y.sup - gv.WORLD_Y.inf)
    y_draw = (y - gv.WORLD_Y.inf) * step
    return gv.HEIGHT - y_draw


def draw2real_x(x):
    """
        Function to convert an x value from the window frame to the world
        :param x : x value of the window frame
        :return x_real : corresponding value in the world
    """
    step = abs(gv.WORLD_X.sup - gv.WORLD_X.inf) / float(gv.WIDTH)
    x_real = x * step + gv.WORLD_X.inf
    return x_real


def draw2real_y(y):
    """
        Function to convert an y value from the window frame to the world
        :param y : y value of the window frame
        :return y_real : corresponding value in the world
    """
    step = abs(gv.WORLD_Y.sup - gv.WORLD_Y.inf) / float(gv.HEIGHT)
    y_real = (gv.HEIGHT - y) * step + gv.WORLD_Y.inf
    return y_real


def resize_event(event):
    """
        Function to get the new size of the window and to update the corresponding global variables
        :param event : the event that generate the function call
    """
    gv.WIDTH = event.width
    gv.HEIGHT = event.height
    draw()


def draw_box(x, y, color_fill='white', color_outline='white'):
    """
        Function to draw a Box on the DRAWING canvas
        :param x : the x interval of the box to draw
        :param y : the y interval of the box to draw
        :param color_fill : the fill color of the box
        :param color_outline : the outline color of the box
    """
    x1 = real2draw_x(x.sup)
    y1 = real2draw_y(y.inf)
    x2 = real2draw_x(x.inf)
    y2 = real2draw_y(y.sup)
    if x1 < 0:
        x1 = 0
    if y1 < 0:
        y1 = 0
    if x2 < 0:
        x2 = 0
    if y2 < 0:
        y2 = 0
    gv.DRAWING.create_rectangle(x1, y1, x2, y2, fill=color_fill, outline=color_outline, width=2)


def draw_sensor():
    """
        Function to draw the global SENSOR on the DRAWING canvas
    """
    x1 = real2draw_x(gv.SENSOR.get_private_robot().get_private_x() - gv.SENSOR.get_range())
    y1 = real2draw_y(gv.SENSOR.get_private_robot().get_private_y() - gv.SENSOR.get_range())
    x2 = real2draw_x(gv.SENSOR.get_private_robot().get_private_x() + gv.SENSOR.get_range())
    y2 = real2draw_y(gv.SENSOR.get_private_robot().get_private_y() + gv.SENSOR.get_range())

    # display the range of the sensor
    gv.DRAWING.create_oval(x1, y1, x2, y2, fill='')

    # display the landmarks of the environment
    for ld in gv.SENSOR.get_private_landmarks():
        x1, y1 = real2draw_x(ld.x) - 2, real2draw_y(ld.y) - 2
        x2, y2 = real2draw_x(ld.x) + 2, real2draw_y(ld.y) + 2
        gv.DRAWING.create_oval(x1, y1, x2, y2, fill='black')

    # display the sensor measurements
    i = 0
    for msr in gv.SENSOR.get_measurements():
        if msr > -1:
            xr = real2draw_x(gv.SENSOR.get_private_robot().get_private_x())
            yr = real2draw_y(gv.SENSOR.get_private_robot().get_private_y())
            xm = real2draw_x(gv.SENSOR.get_private_landmarks()[i].x)
            ym = real2draw_y(gv.SENSOR.get_private_landmarks()[i].y)
            gv.DRAWING.create_line(xr, yr, xm, ym, fill='red')
        i += 1


def draw_robot():
    """
        Function to draw the global ROBOT on the DRAWING canvas
    """
    # for the 'body' of the robot
    x1 = real2draw_x(gv.ROBOT.get_private_x() - gv.ROBOT.get_private_l() / 2.0)
    y1 = real2draw_y(gv.ROBOT.get_private_y() - gv.ROBOT.get_private_l() / 2.0)
    x2 = real2draw_x(gv.ROBOT.get_private_x() + gv.ROBOT.get_private_l() / 2.0)
    y2 = real2draw_y(gv.ROBOT.get_private_y() + gv.ROBOT.get_private_l() / 2.0)
    # for the 'head' of the robot
    xh = gv.ROBOT.get_private_x() + cos(gv.ROBOT.get_private_theta()) * real2draw_x(gv.ROBOT.get_private_l() * 2)
    yh = gv.ROBOT.get_private_y() + sin(gv.ROBOT.get_private_theta()) * real2draw_x(gv.ROBOT.get_private_l() * 2)
    xh1, yh1 = real2draw_x(xh - gv.ROBOT.get_private_l() / 4.0), real2draw_y(yh - gv.ROBOT.get_private_l() / 4.0)
    xh2, yh2 = real2draw_x(xh + gv.ROBOT.get_private_l() / 4.0), real2draw_y(yh + gv.ROBOT.get_private_l() / 4.0)
    # draw the body
    gv.DRAWING.create_oval(x1, y1, x2, y2, fill='grey', outline='black')
    # draw the head
    gv.DRAWING.create_oval(xh1, yh1, xh2, yh2, fill='black', outline='black')


def draw_i_landmarks():
    """
        Function to draw the known position of the landmarks
    """
    for ild in gv.I_LANDMARKS:
        draw_box(ild.x, ild.y, color_fill='', color_outline='green')


def draw_i_pose():
    """
        Function to draw the known pose of the robot
    """
    draw_box(gv.I_POSE.x, gv.I_POSE.y, color_fill='', color_outline='blue')


def draw():
    """
        Function to update the display in the DRAWING canvas
    """
    gv.DRAWING.delete("all")
    draw_i_landmarks()
    if gv.MODE == 1:  # mode 1 to display the robot and the sensor/landmarks
        draw_sensor()
        draw_robot()
    draw_i_pose()
