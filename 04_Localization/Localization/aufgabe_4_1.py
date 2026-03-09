

import sys
sys.path.append("..")
sys.path.append(".")
from FMLRobot import FMLRobot
from FMLCamera import FMLCamera
from map import MAP
import numpy as np
import time


camera = FMLCamera()
map = MAP()
## Define the position of the Aruco codes in the map in dm
map.marker_positions = {
    4: (2.5, 10),
    3: (10, 7.5),
}
with FMLRobot() as robot:
    ## Define the robot position in meters
    robot.position = [0.25, 0, np.pi/2]
    ## Position of the robot in the map
    map.robot_position = [2.5, 0]
    
    robot.navigate_to_aruco_simple(
        camera=camera,
        target_id=4,
        map_object=map            #  ArUco I     
    )
    time.sleep(0.05)
    print("Arrived at 1st Aruco position")
    robot.turn(-90)
    robot.navigate_to_aruco_simple(
        camera=camera,
        target_id=3,
        map_object=map               #  ArUco II     
    )