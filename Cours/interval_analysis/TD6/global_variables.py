from interval.interval import Interval
from TD6.robot import Robot
from TD6.sensor import Sensor
from interval.ipose import IPose

"""
    File that contains the "declaration" of all the global variables of the simulator
    You do not need to modify this file
"""

# the bounded environment where the robot is moving
WORLD_X = Interval(0, 0)
WORLD_Y = Interval(0, 0)

# the simulated robot
ROBOT = Robot()

# the simulated robot's sensor, and the landmarks associated
SENSOR = Sensor(ROBOT, 0, 0)

# the computed position of the robot ([x], [y], [theta])
I_POSE = IPose()

# the known positions of the landmarks [([x1],[y1]),([x2],[y2]),...]
I_LANDMARKS = []

# the width and height size of the window frame
WIDTH = 50
HEIGHT = 50

# the tkinter canvas to display the items
DRAWING = 0

# to handle the drawing mode
MODE = 0
