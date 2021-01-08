from TD6.display_functions import *
from TD6.init_functions import *
from TD6.work2do import *
from interval.interval import Interval
import TD6.global_variables as gv

import tkinter as tk

"""
    The main file of the simulator
"""

# size of the displayed area
gv.WORLD_X = Interval(0, 10000)
gv.WORLD_Y = Interval(0, 10000)

init_robot()  # initialisation of the ROBOT values
init_sensor()  # initialisation of the SENSOR values

mode = 1


def btn_test_event(_):
    print("Test button has been pressed")


def m_key(event):
    if gv.MODE == 1:
        gv.MODE = 0
    elif gv.MODE == 0:
        gv.MODE = 1
    draw()  # update the display
    return event


def down_key(event):
    # moves the robot randomly inside the box ([1000,9000][1000,9000])
    vl, vr = gv.ROBOT.move_random_in_box(1000, 9000, 1000, 9000)
    gv.SENSOR.update_measurements()  # update the measurements
    compute_i_pose(vl, vr)  # compute the new IPose according to the wheel speeds command

    # tests if the I_POSE contain the robot pose
    if not gv.ROBOT.is_in(gv.I_POSE):
        print("ERROR!!!")  # if not, something is wrong with the compute_i_pose() function...
        print(gv.I_POSE)
        print(gv.ROBOT)
    draw()  # update the display
    return event


# creation of the window
window = tk.Tk()
window.title("Wheeled Robot Simulation")  # define the name of the window
window.geometry("500x500+100+50")  # define the original size and position of the window
gv.DRAWING = tk.Canvas(window, background='white')  # define the background color
gv.DRAWING.pack(fill=tk.BOTH, expand=tk.YES, side=tk.TOP)
gv.DRAWING.bind('<Configure>', resize_event)  # get the resize event

btnTest = tk.Button(window, text="Test")  # creation of the Test button
btnTest.pack(fill=tk.X, side=tk.BOTTOM)  # add the button
btnTest.bind('<Button-1>', btn_test_event)  # set the btn event

window.bind('<Down>', down_key)
window.bind('<m>', m_key)

print("press 'm' to display the robot and the landmarks")
print("press 'DOWN' to randomly move the robot")
# call of the loop to display the window
window.mainloop()
