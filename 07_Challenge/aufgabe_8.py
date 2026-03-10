import sys
sys.path.append("..")
sys.path.append(".")
from FMLRobot import FMLRobot
from FMLCamera import FMLCamera
from FMLMqtt import FMLMqtt
from FMLController import PIController
import time

def doTask(robot : FMLRobot,mqtt : FMLMqtt,camera: FMLCamera):
    """
    Task 8: Navigate to charging station, avoiding obstacles.
    1. Follow the line until a blue marker is detected.
    2. After the blue marker, drive straight without line following.
    3. If an obstacle is detected, wait for it to be removed.
    4. Drive for a fixed duration to reach the charging station.
    """
    print("--- Starting Task 8: Drive to charging station ---")

    # Helper function to follow a line until a specific color is detected
    def follow_line_until_color(robot, target_color, controller, velocity):
        print(f"Following line, looking for color: {target_color}...")
        
        # Start driving to avoid getting stuck on the current color
        robot.BP.set_motor_dps(robot.left_motor, velocity)
        robot.BP.set_motor_dps(robot.right_motor, velocity)
        time.sleep(0.5) 
        
        while True:
            # Check if the target color is detected
            current_color = robot.get_color_left()
            if current_color == target_color:
                print(f"Target color detected: {target_color}. Stopping.")
                robot.stop()
                break

            # Standard PI line following logic
            try:
                current_sensor_value = robot.BP.get_sensor(robot.right_sensor)
                u = controller.get_u(current_sensor_value)
                
                # Limit motor speed difference
                if velocity + abs(u) > 500:
                    u = (500 - velocity) if u >= 0 else (velocity - 500)

                # Set motor speeds
                if u >= 0:
                    robot.BP.set_motor_dps(robot.right_motor, velocity - abs(u))
                    robot.BP.set_motor_dps(robot.left_motor, velocity + abs(u))
                else:
                    robot.BP.set_motor_dps(robot.right_motor, velocity + abs(u))
                    robot.BP.set_motor_dps(robot.left_motor, velocity - abs(u))
            except Exception:
                pass # Ignore occasional sensor reading failures
                
            time.sleep(0.01)

    # ================= Task 8 Main Logic =================

    # 1. Initialize controller and velocity for line following
    line_controller = PIController(kp=1.2, ki=0.0, target_value=50.0)
    velocity = 150

    # 2. Follow the line to the blue marker
    print("========== Stage 1: Following line to blue marker ==========")
    follow_line_until_color(robot, "Blue", line_controller, velocity)
    print("Reached the blue marker.")

    # 3. Drive straight with obstacle avoidance
    print("========== Stage 2: Driving straight to charging station with obstacle avoidance ==========")
    
    DRIVE_DURATION_S = 10  # Drive for 10 seconds to reach the charging station (tune as needed)
    OBSTACLE_DISTANCE_CM = 20 # Distance to consider as an obstacle

    start_time = time.time()
    while time.time() - start_time < DRIVE_DURATION_S:
        # Check for obstacles
        distance = robot.get_distance_front()
        
        if distance != -1 and distance < OBSTACLE_DISTANCE_CM:
            print(f"Obstacle detected at {distance} cm. Stopping and waiting.")
            robot.stop()
            
            # Wait until the obstacle is removed
            while True:
                distance = robot.get_distance_front()
                if distance == -1 or distance >= OBSTACLE_DISTANCE_CM:
                    print("Obstacle removed. Resuming journey.")
                    break
                print("Still waiting for obstacle to be removed...")
                time.sleep(0.5)
        
        # Drive forward
        print("Driving forward...")
        robot.BP.set_motor_dps(robot.left_motor, velocity)
        robot.BP.set_motor_dps(robot.right_motor, velocity)
        
        time.sleep(0.1)

    # 4. Reached destination
    robot.stop()
    print("========== Task 8 Finished: Arrived at charging station ==========")

