import sys
sys.path.append("..")
sys.path.append(".")
from FMLRobot import FMLRobot
import time
import numpy as np
import math

with FMLRobot() as robot:
    robot.drive(2)
    robot.drive(-2)
    robot.turn(360)
    robot.turn(-360)

