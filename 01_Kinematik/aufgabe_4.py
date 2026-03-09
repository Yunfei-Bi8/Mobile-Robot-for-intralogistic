import sys
sys.path.append("..")
sys.path.append(".")
from FMLRobot import FMLRobot
import time
import numpy as np
import math

with FMLRobot() as robot:
    print(f"initial position {robot.position}")
    robot.drive(0.5)
    print(f"driven 0.5 forward leading to {robot.position}")
    robot.drive(-0.3)
    print(f"driven -0.3 backwards leading to {robot.position}")
    robot.turn(180)
    print(f"turned 180 degrees forward leading to {robot.position}")
    robot.turn(-180)
    print(f"turned -180 degrees forward leading to {robot.position}")