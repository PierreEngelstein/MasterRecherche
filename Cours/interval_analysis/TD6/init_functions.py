import TD6.global_variables as gv
from interval.ifunctions import *
from TD6.sensor import Sensor
import math as math
from TD6.landmark import Landmark


"""
    File that contains functions to initialize the simulation
    You do not need to modify this file
"""


def init_robot():
    """
        function to init the robot values and the initial i_pose
    """
    l_dst = 200.0  # distance between the wheels
    err_l = 5.0  # imprecision over the l value
    err_position = 10.0  # initial position error
    x_aim = 5000  # wanted initial x position of the robot
    y_aim = 5000  # wanted initial x position of the robot
    theta_aim = 0  # wanted initial orientation of the robot
    x = rd.uniform(x_aim - err_position, x_aim + err_position)  # initial x position
    y = rd.uniform(y_aim - err_position, y_aim + err_position)  # initial y position
    err_theta = 1 * math.pi / 108  # initial orientation error
    theta = rd.uniform(theta_aim - err_theta, theta_aim + err_theta)  # initial orientation
    v_max = 200.0  # maximal wheel speed
    delta_t = 1.0  # time step between two position update
    drift = 1.0  # error over the command and the wheel speed
    err_odo = 0  # imprecision over the odometry value
    err_compass = 5 * math.pi / 180  # imprecision over the compass value

    gv.ROBOT.init_robot(x, y, theta, l_dst, err_l, v_max, drift, delta_t, err_odo, err_compass)

    gv.I_POSE.x = Interval(x_aim - err_position, x_aim + err_position)
    gv.I_POSE.y = Interval(y_aim - err_position, y_aim + err_position)
    gv.I_POSE.theta = Interval(theta_aim - err_theta, theta_aim + err_theta)


def init_sensor():
    """
        function to init the sensor
    """
    range_sensor = 2000
    precision = 10
    nb_landmarks = 20
    error_landmarks_position = 800
    gv.SENSOR = Sensor(gv.ROBOT, range_sensor, precision)
    init_landmarks(nb_landmarks, error_landmarks_position)


def init_landmarks(nb_landmarks, error):
    """
        Function that initialize the landmarks of the environment

        :param nb_landmarks : the number of landmarks we want
        :param error : the +/- incertitude we have over the landmark position
    """

    del gv.I_LANDMARKS[:]
    # first we generate random landmarks in the map
    gv.SENSOR.init_landmarks_randomly(nb_landmarks, gv.WORLD_X.inf, gv.WORLD_X.sup, gv.WORLD_Y.inf,
                                      gv.WORLD_Y.sup)

    # Then we get the Interval Positions of those landmarks according to the error
    for i in range(0, nb_landmarks):
        x_inf, x_sup, y_inf, y_sup = gv.SENSOR.get_landmark_position(i, error)
        gv.I_LANDMARKS.append(Landmark(Interval(x_inf, x_sup), Interval(y_inf, y_sup)))
