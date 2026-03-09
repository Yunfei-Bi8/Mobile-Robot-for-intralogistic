import sys
sys.path.append("..")
sys.path.append(".")
from FMLRobot import FMLRobot
import time



with FMLRobot() as robot:
    # pass
    while True:

        color1 = robot.get_color_left()
        time.sleep(0.1)
        color2 = robot.get_color_left()

        if color1 == color2:
            print(f"color {color1} detected")
        else:
            print("color not reliably detected")

        time.sleep(0.3)
# Check the sensor value left and right to be sure that we measured the right thing.
