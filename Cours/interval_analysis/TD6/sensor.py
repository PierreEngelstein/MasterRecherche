import random as rd
from math import *
from TD6.landmark import Landmark

""" You do not need to modify this file """


class Sensor:
    """ a 'Sensor' class
        provides the distance between the robot and the landmarks if the landmarks are closed enough (in range)
    """

    def __init__(self, robot, range_sensor, error):
        """
        Constructor

        :param robot: the robot where the sensor is
        :param range_sensor: the range of the sensor (max distance to detect landmark)
        :param error: the precision of the sensor
        """

        self._landmarks = []  # the landmarks of the environment
        self._measurements = []  # the measurements data
        self._robot = robot  # the robot associated to the sensor
        self._range = range_sensor  # the range of the sensor
        self._error = error  # the precision of the measurements

    def init_landmarks_randomly(self, nb_landmarks, x_inf, x_sup, y_inf, y_sup):
        """
        :param nb_landmarks: number of wanted landmarks
        :param x_inf: the minimal x position of the landmarks
        :param x_sup: the maximal x position of the landmarks
        :param y_inf: the minimal y position of the landmarks
        :param y_sup: the maximal y position of the landmarks
        """
        del self._landmarks[:]  # the previous landmarks are erased
        del self._measurements[:]
        for i in range(0, nb_landmarks):
            x = rd.uniform(x_inf, x_sup)
            y = rd.uniform(y_inf, y_sup)
            self._landmarks.append(Landmark(x, y))
            self._measurements.append(-1)  # we add a measurement for each landmark

    def get_error(self):
        """
        Function to get the sensor precision
        :return: the _error value of the sensor
        """
        return self._error

    def get_range(self):
        """
        Function to get the range of the sensor
        :return: the _range value of the sensor
        """
        return self._range

    def update_measurements(self):
        """
        Function to update the measurement values according to the landmarks
        if a landmark is too far from the sensor, the value is -1, otherwise it is the distance between them
        """
        i = 0
        for ld in self._landmarks:
            dst = sqrt((ld.x - self._robot.get_private_x()) ** 2 + (ld.y - self._robot.get_private_y()) ** 2)
            dst_err = rd.uniform(dst - self._error, dst + self._error)
            if dst <= self._range:
                self._measurements[i] = dst_err
            else:
                self._measurements[i] = -1
            i += 1

    def get_landmark_position(self, i, error):
        """
        Function to get a box over a landmark position according to an incertitude
        :param i: the index of the landmark we want the box of
        :param error: the precision over the landmark position (the "size of the box")
        :return:  x_inf, x_sup, y_inf, y_sup : the box containing the landmark
        """
        if 0 <= i < len(self._landmarks):
            # we don't want the box to be centered over the landmark
            rex = rd.uniform(0, error)
            rey = rd.uniform(0, error)
            x_inf = self._landmarks[i].x - rex
            x_sup = self._landmarks[i].x + error - rex
            y_inf = self._landmarks[i].y - rey
            y_sup = self._landmarks[i].y + error - rey

            return x_inf, x_sup, y_inf, y_sup
        else:
            print("SENSOR -  ERROR index out of range")
            return 0, 0, 0, 0

    def get_measurement(self, i):
        """
        Function to get a measurement value, the index of the measurement correspond to the landmark
        :param i: the index of the required measurement
        :return: the measurement value
        """
        if 0 <= i < len(self._measurements):
            return self._measurements[i]
        else:
            print("SENSOR -  ERROR index out of range")
            return -2

    def get_measurements(self):
        """
        Function to get a all the measurements
        """
        return self._measurements

    def get_private_robot(self):
        """
        Function to get the robot associated to the sensor
        Should only be used for display purpose!
        """
        return self._robot

    def get_private_landmarks(self):
        """
        Function to get the landmarks associated to the sensor
        Should only be used for display purpose!
        """
        return self._landmarks
