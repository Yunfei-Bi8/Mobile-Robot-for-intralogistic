import sys
sys.path.append("..")
sys.path.append(".")
from FMLRobot import FMLRobot
import time



with FMLRobot() as robot:
    while True:
        print(f"Distance: {robot.get_distance_front()}")
        time.sleep(0.5)

