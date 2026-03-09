import sys
sys.path.append("..")
sys.path.append(".")
from FMLRobot import FMLRobot
import time


with FMLRobot() as robot:
    robot.move_fork(300) # Play around until you know how many degrees you need to turn

# Also check the lift_fork() and drop_fork() functions
    #robot.lift_fork()
    #robot.drop_fork()