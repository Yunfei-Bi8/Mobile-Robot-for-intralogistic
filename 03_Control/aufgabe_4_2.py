import sys
sys.path.append("..")
sys.path.append(".")
from FMLRobot import FMLRobot
from FMLController import PIController
import time


pi_controller = PIController(kp=4,ki=0.25,target_value=30.0)
with FMLRobot() as robot:
    robot.follower_line(velocity=300,controller=pi_controller)
