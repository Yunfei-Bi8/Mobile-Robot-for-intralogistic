import sys
import time
import math
import curses
import numpy as np
sys.path.append(".")
sys.path.append("..")
import matplotlib.pyplot as plt
from FMLRobot import FMLRobot

#plt.ion()  # Enable interactive mode for real-time plotting
# Grid dimensions
GRID_SIZE = 10
RESOLUTION = 0.1  # Each grid cell represents 10cm
DISTANCE = 0.1
ANGLE = 45

# To keep the task easy we will stop the mapping while the robot is turning
turning = False 

# Initialize the map
map = np.full((GRID_SIZE, GRID_SIZE), 0.5)  # 0.5 means unknown

# Robot starting position in map
x_robot_0 = 1.0
y_robot_0 = 1.0
phi_robot_0 = 0

x = list() # Start x coordinate list
y = list() # Start y coordinate list

# Define axis limits
plt.axis([0, 10, 0, 10])
plt.axis([0, 10, 0, 10])

def update_map(robot, turning):
    # The robot odometry system starts its pose in x,y,phi = 0 
    # But the initial robot coordinates are given by x_robot_0, y_robot_0, phi_robot_0
    # Calculate the new robot pose by adding the odometry pose to the initial pose
    robot_odom_pose_x = None # Hint: The object robot has a member called position that contains the updated odometry values [x, y, phi]  
    robot_odom_pose_y = None
    robot_odom_pose_phi = None
    robot_odom_pose_x, robot_odom_pose_y, robot_odom_pose_phi = robot.position
    robot_x = x_robot_0 + robot_odom_pose_x * 10
    robot_y = y_robot_0 + robot_odom_pose_y * 10
    robot_phi = phi_robot_0 + robot_odom_pose_phi

    x.append(robot_x + 0.5)
    y.append(robot_y + 0.5)

    # The sensor phi is located pi/2 radians to the right of the robot
    # so its orientation is the orientation of the robot - pi/2 
    sensor_phi = - np.pi/2 + robot_phi

    # Mapping =  get distance with ultrasonic sensor in the current position
    right_distance = round(robot.get_distance_right()/10) # Distance to the obstacle in dm
    obstacle_x = min(robot_x + right_distance*math.cos(sensor_phi), 10) # The obstacle in x is the position of the robot + the distance to the obstacle
    obstacle_y = min(robot_y + right_distance*math.sin(sensor_phi), 10) # The obstacle in y is the position of the robot + the distance to the obstacle
    
    max_x = round(max(0, obstacle_x)) # The x coordinate for the obstacle should be limited between 0 and the obstacle coordinate
    max_y = round(max(0, obstacle_y)) # The y coordinate for the obstacle should be limited between 0 and the obstacle coordinate
    # max_x = int(np.clip(obstacle_x, 0, GRID_SIZE - 1))
    # max_y = int(np.clip(obstacle_y, 0, GRID_SIZE - 1))
    robot_i_x = round(robot_x)
    robot_i_y = round(robot_y)
    # robot_i_x = int(np.clip(robot_x, 0, GRID_SIZE - 1))
    # robot_i_y = int(np.clip(robot_y, 0, GRID_SIZE - 1))
    # Iterate the map until the obstacle position to clear the path until the obstacle
    if not turning:
        for i_y in range(min(robot_i_y, max_y), max(robot_i_y, max_y)+ 1):
            for i_x in range(min(robot_i_x, max_x), max(robot_i_x, max_x) + 1):   
                # If the cell is unknown or an obstacle:        
                if map[i_y][i_x] == 0.5:
                    map[i_y][i_x] = 1.0 # clear the cell

        # Make the obstacle cell equal to 0 
        map[max_y][max_x] = 0.0

    # Update the map.
    save_map(map, x ,y)

def save_map(grid, x, y, filename=f"map_4_2.png"):
    """Save the occupancy grid as an image file."""
    plt.imshow(grid, cmap="gray", origin="lower", vmin=0, vmax=1, extent=[0, GRID_SIZE, 0, GRID_SIZE])
    plt.title("Occupancy Grid Map")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.plot(x, y, color = 'b')
    #plt.pause(0.01) # Update the plot
    plt.savefig(filename)
    plt.close()

def teleop(stdscr, turning):
    # Print instructions with arrows
    instructions = [
        "Teleop mode enabled. Use the arrow keys to control the robot:",
        "    ↑ : Move forward (0.05m)",
        "← : Turn left (45°)            → : Turn right (-45°)",
        "    ↓ : Move backward (0.05m)",
        "Press 'q' to exit."
    ]
    
    # Display instructions in the console
    for idx, line in enumerate(instructions):
        stdscr.addstr(idx, 0, line)
    
    stdscr.refresh()
    stdscr.nodelay(True)  # Non-blocking input
    stdscr.keypad(True)   # Enable arrow keys
    
    with FMLRobot() as robot:
        update_map(robot, turning)
        while True:
            key = stdscr.getch()  # Get key press
            if key == curses.KEY_UP:
                stdscr.addstr(len(instructions) + 1, 0, "Moving forward      ")
                robot.drive(DISTANCE)  # Move forward 0.05 meters
                update_map(robot, turning)
            elif key == curses.KEY_DOWN:
                stdscr.addstr(len(instructions) + 1, 0, "Moving backward     ")
                robot.drive(-DISTANCE)  # Move backward 0.05 meters
                update_map(robot, turning)
            elif key == curses.KEY_LEFT:
                stdscr.addstr(len(instructions) + 1, 0, "Turning left        ")
                robot.turn(ANGLE)  # Turn 45 degrees to the left
                turning = not turning
                update_map(robot, turning)
            elif key == curses.KEY_RIGHT:
                stdscr.addstr(len(instructions) + 1, 0, "Turning right       ")
                robot.turn(-ANGLE)  # Turn 45 degrees to the right
                turning = not turning
                update_map(robot, turning)
            elif key == ord('q'):
                stdscr.addstr(len(instructions) + 1, 0, "Exiting teleop mode.")
                break
            stdscr.refresh()
    
if __name__ == "__main__":
    turning = False 
    curses.wrapper(teleop, turning)