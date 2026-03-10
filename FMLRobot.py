


import brickpi3
import time
import math
import numpy as np
from FMLController import PIController
class FMLRobot:
    def _init_motors(self):
        self.left_motor = self.BP.PORT_D
        self.right_motor = self.BP.PORT_A
        self.fork_motor = self.BP.PORT_B
        self.BP.set_motor_limits(self.left_motor, dps = 300)
        self.BP.set_motor_limits(self.right_motor, dps = 300)
        self.BP.set_motor_limits(self.fork_motor, dps = 400)

    def _init_sensors(self):
        self.left_sensor = self.BP.PORT_4
        self.right_sensor = self.BP.PORT_3
        self.front_sensor = self.BP.PORT_1
        self.side_sensor = self.BP.PORT_2
        self.BP.set_sensor_type(self.front_sensor, self.BP.SENSOR_TYPE.EV3_ULTRASONIC_CM)
        self.BP.set_sensor_type(self.side_sensor, self.BP.SENSOR_TYPE.EV3_ULTRASONIC_CM)
        self.BP.set_sensor_type(self.right_sensor, self.BP.SENSOR_TYPE.EV3_COLOR_REFLECTED)
        # self.BP.set_sensor_type(self.BP.PORT_3, self.BP.SENSOR_TYPE.EV3_COLOR_COLOR)
        self.BP.set_sensor_type(self.left_sensor, self.BP.SENSOR_TYPE.EV3_COLOR_COLOR)

    def _init_constants(self):
        self.colors = { 0:"None", 1:"Black", 2:"Blue", 3:"Green", 4:"Yellow", 5:"Red", 6:"White", 7:"Brown" }
        self.last_color_left = 0
        self.last_color_right = 0

    # To be implemented in 01 - Kinematik
    def _init_kinematik(self):
        self.wheel_radius = 0.0344
        self.wheel_distance = 0.144
        self.wheel_circumference = 2*math.pi*0.0344
        self.gear_ratio = 3
        
        # global position of the robot within the coordinate system [x,y,phi]
        self.position = [0.0,0.0,0.0]
        
        # last encoder values are saved in the object (read out the encoder when starting the robot)
        self.encoder_left = self.BP.get_motor_encoder(self.left_motor)
        self.encoder_right= self.BP.get_motor_encoder(self.right_motor)

    # Constructor (gets called on object creation -> FMLRobot())
    def __init__(self):
        self.BP = brickpi3.BrickPi3()
        self._init_motors()
        self._init_sensors()
        self._init_constants()
        time.sleep(4.0)
        self._init_kinematik()


    # context manager entry point
    def __enter__(self):
        return self

    # context manager exit point --> gets called on exit of with block
    def __exit__(self, exc_type, exc_value, traceback):
        # Stop the motors and reset the sensors etc
        self.BP.reset_all()
    
    
    #todo in aufgabe 4
    # def get_distance_from_encoder(self):
    #     # read out encoder
    #     new_encoder_left = self.BP.get_motor_encoder(self.left_motor)
    #     new_encoder_right = self.BP.get_motor_encoder(self.right_motor)
    #     # compute the difference
    #     encdelta_right =  new_encoder_right-self.encoder_right 
    #     encdelta_left = new_encoder_left- self.encoder_left
    #     #calculating driven distance
    #     dis_right = None
    #     dis_left = None
    #     # update the encoder values 
    #     self.encoder_left = None
    #     self.encoder_right = None

    #     return (dis_left,dis_right) # delta s_r delta s_l
    
    def get_distance_from_encoder(self):
        # read out encoder
        new_encoder_left = self.BP.get_motor_encoder(self.left_motor)
        new_encoder_right = self.BP.get_motor_encoder(self.right_motor)
        
        # compute the difference (how many degrees the motor turned since last check)
        encdelta_right = new_encoder_right - self.encoder_right 
        encdelta_left = new_encoder_left - self.encoder_left
        
        # calculating driven distance in meters
        # formula: (motor_degrees / gear_ratio / 360) * circumference
        dis_right = (encdelta_right / self.gear_ratio / 360.0) * self.wheel_circumference
        dis_left = (encdelta_left / self.gear_ratio / 360.0) * self.wheel_circumference
        
        # update the encoder values for the next time this function is called
        self.encoder_left = new_encoder_left
        self.encoder_right = new_encoder_right

        return (dis_left, dis_right) # delta s_l, delta s_r

    # odometrie
    # def update_position(self):
    #     delta_s_left, delta_s_right = self.get_distance_from_encoder()
    #     delta_s = None

    #     delta_x = None
    #     delta_y = None
    #     delta_phi = None
        
    #     # update the position
    #     self.position[0]= None # X
    #     self.position[1]= None # Y
    #     self.position[2]= None # phi
        
    # odometrie
    def update_position(self):
        # delta_s_left is delta s_L, delta_s_right is delta s_R
        delta_s_left, delta_s_right = self.get_distance_from_encoder()
        
        # Average distance traveled by the center of the robot
        delta_s = (delta_s_left + delta_s_right) / 2.0

        # Change in orientation (phi)
        # L is self.wheel_distance
        delta_phi = (delta_s_right - delta_s_left) / self.wheel_distance
        
        # Calculate X and Y displacement based on the CURRENT orientation
        # self.position[2] is the current phi angle before updating
        delta_x = delta_s * math.cos(self.position[2])
        delta_y = delta_s * math.sin(self.position[2])
        
        # Update the global position [x, y, phi]
        self.position[0] += delta_x      # X
        self.position[1] += delta_y      # Y
        self.position[2] += delta_phi    # phi
    
    def stop(self):
        self.BP.set_motor_dps(self.left_motor, 0)
        self.BP.set_motor_dps(self.right_motor, 0)
       

    # To be implemented in 1.1
    # def turn(self,degree):
    #     # needed motor rotation to achieve movement 
    #     deg_right = 0
    #     deg_left = 0
    #     #turning
    #     self.BP.set_motor_position_relative(self.left_motor, deg_left)
    #     self.BP.set_motor_position_relative(self.right_motor, deg_right)
        
    #     # give motors some time to spin
    #     time.sleep(0.5)

    #     # read motor veloctiy until zero --> robot stands -> we can return from the function
    #     while self.BP.get_motor_status(self.left_motor)[3] != 0:
    #         time.sleep(0.02)
    
    def turn(self, degree):
      # needed motor rotation to achieve movement
      deg_right = self.gear_ratio*(self.wheel_distance/(2*self.wheel_radius))*degree
      deg_left = -deg_right

      # turning
      self.BP.set_motor_position_relative(self.left_motor, deg_left)
      self.BP.set_motor_position_relative(self.right_motor, deg_right)

      # give motors some time to spin
      time.sleep(0.5)

      # read motor velocity until zero --> robot stands still, we can return from the function
      while self.BP.get_motor_status(self.left_motor)[3] != 0:
        time.sleep(0.02)
      self.update_position()
     

    # # To be implemented in 1.1
    # def drive(self, distance):
    #     # needed motor rotation to achieve movement
    #     delta_angle = 0
    #     # add angle to current motor position
    #     self.BP.set_motor_position_relative(self.left_motor, delta_angle)
    #     self.BP.set_motor_position_relative(self.right_motor, delta_angle)
        
    #     # give motors some time to spin
    #     time.sleep(0.5)
    #     # read motor veloctiy until zero --> robot stands -> we can return from the function
    #     while self.BP.get_motor_status(self.left_motor)[3] != 0:
    #         time.sleep(0.02)

    def drive(self, distance):
      # needed motor rotation to achieve movement
      delta_angle = 3*distance/self.wheel_radius*180/math.pi

      # add angle to current motor position
      self.BP.set_motor_position_relative(self.left_motor, delta_angle)
      self.BP.set_motor_position_relative(self.right_motor, delta_angle)

      # give motors some time to spin
      time.sleep(0.5)

      # read motor velocity until zero --> robot stands still, we can 
      # return from the function
      while self.BP.get_motor_status(self.left_motor)[3] != 0:
         time.sleep(0.02)
      self.update_position()

    # To be implemented in 2.1
    def get_distance_front(self):
        try:
            # read sensor 
            distance = self.BP.get_sensor(self.front_sensor)
        except brickpi3.SensorError as error:
            # Default wert
            distance = -1 # defaults to None
            print(f"Error during get_distance_front(): {error}")
    
        return distance
    
    ##newly 4.2
    def get_distance_right(self):
        try:
            #read sensor
            distance=self.BP.get_sensor(self.side_sensor)
            print("right dist",distance)
        except brickpi3.SensorError as error:
            distance=-1
            print(f"Error during get_distance_right():{error}")
        return distance
    

    
    ##new1
    def get_distance_side(self):
            try:
                distance = self.BP.get_sensor(self.side_sensor)
            except brickpi3.SensorError as error:
                distance = -1
                print(f"Error during get_distance_side(): {error}")
            return distance

    # To be implemented in 2.1
    def get_color_left(self):
        try:
            color = self.BP.get_sensor(self.left_sensor)
        # If brickpy sensor throws error set default value
        except brickpi3.SensorError as error:
            color = 0 # Default Value and print error
            print(f"Error during get_color_left(): {error}")
    
        # if color == self.last_color_left:
        #     print(f"color {self.colors[color]} detected")
        # else:
        #     print("color not reliably detected")
        
        self.last_color_left = color
        
        time.sleep(0.01)
        return color
        # if color in self.colors:
        #     # color_counter+=1
        #     return self.colors[color]
        # else:
        #     # color_counter=0
        #     return "None"
        # if  color_counter ==2:
        #     return color

    
    # To be implemented in 2.1    
    def get_color_right(self):
        try:
            color = self.BP.get_sensor(self.right_sensor)
        except brickpi3.SensorError as error:
            color = 0 
            print(f"Error during get_color_right(): {error}")
    
        # if color == self.last_color_right:
        #     print(f"color {self.colors[color]} detected")
        # else:
        #     print("color not reliably detected")

        self.last_color_right = color
        if color in self.colors:
            return self.colors[color]
        else:
            return "None"

     
    ## Actor stuff

    # To be implemented in 2.3g
    def lift_fork(self):
        self.move_fork(700)


     # To be implemented in 2.3
    def drop_fork(self):
        self.move_fork(-700)

    # to be implemented in 2.3
    def move_fork(self,degrees):
        # TODO Move fork motor
        # Move fork motor by the specified degrees
        self.BP.set_motor_position_relative(self.fork_motor, degrees)
        # wait on the motor and check if it finished moving
        time.sleep(0.4)
        # read motor veloctiy until zero --> fork lift at position
        while self.BP.get_motor_status(self.fork_motor)[3] != 0:
            time.sleep(0.02)



    ## Higher level functions

    ## Followers:
    def follower_line(self, velocity, controller):
        while True:
            #stopping creteria
            front_distance = self.get_distance_front()
            # If a valid distance is read and it's closer than 15 cm
            if front_distance != -1 and front_distance < 15: 
                print("Obstacle detected! Stopping robot.")
                self.stop()
                break # Exit the line following loop


            # TODO Get reflected light of right sensor
            current_sensor_value = self.BP.get_sensor(self.right_sensor)
            # TODO Calculate steering using Controller algorithm
            u = controller.get_u(current_sensor_value)

            #test
            print("Current sensor value:",current_sensor_value)
            
            # Limit u to 500
            if velocity + abs(u) > 500:
                if u >= 0:
                    u = 500 - velocity
                else:
                    u = velocity - 500

            # Run motors with correction
            if u >= 0:
                self.BP.set_motor_dps(self.right_motor,velocity - abs(u))
                self.BP.set_motor_dps(self.left_motor,velocity + abs(u))
            else:
                self.BP.set_motor_dps(self.right_motor,velocity + abs(u))
                self.BP.set_motor_dps(self.left_motor,velocity - abs(u))
            
            time.sleep(0.01)
        
    
    # def follower_distance(self, velocity, controller, colors_to_stop=[]):
    ##new2
    def follower_distance(self, velocity, controller, colors_to_stop=[]):
        """
        Wall/obstacle following with constant lateral distance using side ultrasonic sensor.
        controller.get_u(measurement_cm) should output steering correction u.
        Convention (same as follower_line):
            u >= 0  -> turn right  (left faster, right slower)
            u <  0  -> turn left
        colors_to_stop: list of color strings, e.g. ["Black"], read from left color sensor.
        """
        while True:
            # stop if line (or any target color) detected again
            if colors_to_stop:
                c_left = self.get_color_left()
                if c_left in colors_to_stop:
                    print(f"Stop color detected: {c_left}")
                    self.stop()
                    break

            # read side distance (cm)
            side_distance = self.get_distance_side()
            if side_distance == -1:
                time.sleep(0.01)
                continue

            # controller output
            u = -controller.get_u(side_distance)

            # saturate so motor dps stays within +/-500 like your line follower
            if velocity + abs(u) > 500:
                if u >= 0:
                    u = 500 - velocity
                else:
                    u = velocity - 500

            # motor mixing (same structure as follower_line)
            if u >= 0:
                self.BP.set_motor_dps(self.right_motor, velocity - abs(u))
                self.BP.set_motor_dps(self.left_motor,  velocity + abs(u))
            else:
                self.BP.set_motor_dps(self.right_motor, velocity + abs(u))
                self.BP.set_motor_dps(self.left_motor,  velocity - abs(u))

            time.sleep(0.01)

    #new3
    def bypass_obstacle(self, velocity, controller_distance,
                       turn_angle_deg=60, target_lateral_cm=15, line_color="Black"):
        """
        BUG2-like avoidance:
          1) rotate by 60°
          2) go straight until lateral distance to obstacle is target_lateral_cm
          3) follow obstacle with constant distance until the line is reached again (color == line_color)
        Assumption: obstacle will be on the robot's RIGHT side during bypass (side_sensor looks right).
        """

        # --- Step 1: rotate 60° ---
        self.stop()
        time.sleep(0.1)
        self.turn(turn_angle_deg)
        self.stop()
        time.sleep(0.1)

        # --- Step 2: drive straight until side distance <= 15 cm ---
        self.BP.set_motor_dps(self.left_motor, velocity)
        self.BP.set_motor_dps(self.right_motor, velocity)

        while True:
            d_side = self.get_distance_side()
            if d_side != -1 and d_side <= target_lateral_cm:
                break

            # safety: if something is directly in front, stop to avoid collision
            d_front = self.get_distance_front()
            if d_front != -1 and d_front < 8:
                print("Safety stop: front too close during approach.")
                break

            time.sleep(0.01)

        self.stop()
        time.sleep(0.1)

        # --- Step 3: follow obstacle at constant distance until line reached again ---
        # Here we stop when left color sensor sees the line again (black).
        self.follower_distance(velocity, controller_distance, colors_to_stop=[line_color])

        self.stop()
    

    # read and display the current voltages
    def print_battery_status(self):
        print("Battery voltage: %6.3f  9v voltage: %6.3f  5v voltage: %6.3f  3.3v voltage: %6.3f" % (self.BP.get_voltage_battery(), self.BP.get_voltage_9v(), self.BP.get_voltage_5v(), self.BP.get_voltage_3v3())) 

    # ---------- 新增函数：基于ArUco标记的简单导航 ----------
    # def navigate_to_aruco_simple(self, camera, target_id=None, target_distance_cm=10, velocity=150, map_object=None):
    #     """
    #     使用ArUco标记导航至目标位置。
    #     通过相机获取偏移量，利用P控制器调整方向，当前方障碍物距离小于target_distance_cm时停止。
    #     每秒保存一次地图快照。
    #     """
    #     from FMLController import PController
    #     controller = PController(kp=1.2, target_value=0)
    #     last_save_time = time.time()
    #     snapshot_id = 0

    #     while True:
    #         offset = camera.get_aruco_offset(target_id=target_id)
    #         front_distance = self.get_distance_front()

    #         # 如果前方距离小于目标距离，并且读数有效，则停止
    #         if front_distance != -1 and front_distance < target_distance_cm:
    #             print(f"Reached target distance: {front_distance} cm")
    #             break

    #         # 如果未检测到目标ArUco，停止（可根据需要扩展搜索逻辑）
    #         if offset is None:
    #             print("No ArUco marker detected, stopping.")
    #             self.stop()
    #             break

    #         # 计算控制量
    #         u = controller.get_u(offset)

    #         # 限制电机速度不超过500
    #         if velocity + abs(u) > 500:
    #             if u >= 0:
    #                 u = 500 - velocity
    #             else:
    #                 u = velocity - 500

    #         # 设置左右电机速度
    #         if u >= 0: # u > 0 means offset is negative (marker to the left) -> Turn Left
    #             self.BP.set_motor_dps(self.right_motor, velocity + abs(u))
    #             self.BP.set_motor_dps(self.left_motor, velocity - abs(u))
    #         else: # u < 0 means offset is positive (marker to the right) -> Turn Right
    #             self.BP.set_motor_dps(self.right_motor, velocity - abs(u))
    #             self.BP.set_motor_dps(self.left_motor, velocity + abs(u))

    #         # 更新机器人位姿（基于编码器）
    #         self.update_position()

    #         # 每秒保存地图快照
    #         current_time = time.time()
    #         if current_time - last_save_time > 1.0:
    #             if map_object is not None:
    #                 # 将位置从米转换为分米（地图单位）
    #                 map_object.robot_position = (self.position[0] * 10, self.position[1] * 10)
    #                 filename = f"map.png"  # 可改为带编号的文件名如 f"map_{snapshot_id:03d}.png"
    #                 map_object.save_map(filename)
    #                 print(f"Saved {filename}")
    #                 snapshot_id += 1
    #                 last_save_time = current_time

    #         time.sleep(0.01)

    #     self.stop()
    def navigate_to_aruco_simple(self, camera, target_id=None, target_distance_cm=10, velocity=150, map_object=None):
        """
        Navigates the robot to a specified ArUco marker.
        It uses a P-controller to adjust the robot's orientation based on the offset provided by the camera.
        The robot stops when it is closer to an obstacle than target_distance_cm.
        A map snapshot is saved every second.
        """
        from FMLController import PController
        controller = PController(kp=1.2, target_value=0)
        last_save_time = time.time()
        snapshot_id = 0

        while True:
            offset = camera.get_aruco_offset(target_id=target_id)
            print("offset is ",offset)
            front_distance = self.get_distance_front()
            #print("front_distance is:",front_distance)
            # Stop if the front_distance is less than target_distance_cm and the reading is valid
            if front_distance != -1 and front_distance < target_distance_cm:
                print(f"Reached target distance: {front_distance} cm. Stopping.")
                #self.stop()
                break

            # If no ArUco marker is detected, stop the robot.
            if offset is None:
                print("No ArUco marker detected, stopping.")
                # self.stop()
                # break

            # Calculate the control value from the P-controller
            u = controller.get_u(offset)

            # Limit the motor speed to a maximum of 500
            if velocity + abs(u) > 500:
                if u >= 0:
                    u = 500 - velocity
                else:
                    u = velocity - 500

            # Set the motor speeds
            if u >= 0: # u > 0 means offset is negative (marker to the left) -> Turn Left
                self.BP.set_motor_dps(self.right_motor, velocity - abs(u))
                self.BP.set_motor_dps(self.left_motor, velocity + abs(u))
            else: # u < 0 means offset is positive (marker to the right) -> Turn Right
                self.BP.set_motor_dps(self.right_motor, velocity + abs(u))
                self.BP.set_motor_dps(self.left_motor, velocity - abs(u))

            # Update the robot's position using odometry
            self.update_position()

            # Save a map snapshot every second
            current_time = time.time()
            if current_time - last_save_time > 1.0:
                if map_object is not None:
                    # Convert position from meters to decimeters for the map
                    map_object.robot_position = (self.position[0] * 10, self.position[1] * 10)
                    filename = f"map_{snapshot_id:03d}.png"
                    map_object.save_map(filename)
                    print(f"Saved {filename}")
                    snapshot_id += 1
                    last_save_time = current_time

            time.sleep(0.01)

        self.stop()


    def debouncing(get_color_func, threshold=2, delay=0.01):
        """
        正确的颜色去抖动函数
        
        :param get_color_func: 一个用于读取当前颜色的函数（必须能动态返回新值）
        :param threshold: 确认颜色所需的连续相同次数（默认2次）
        :param delay: 每次读取之间的间隔时间（秒）
        """
        last_color = get_color_func() # 获取初始颜色
        color_counter = 0
        
        while True:
            # 1. 动态读取新的颜色值
            current_color = get_color_func() 
            
            # 2. 判断是否和上一次的颜色相同
            if current_color == last_color:
                color_counter += 1
            else:
                color_counter = 0
                # 注意：一旦发现颜色不一样，必须把最新的颜色设为基准！
                last_color = current_color 
                
            # 3. 连续相同次数达到阈值，判定颜色稳定，返回该颜色
            if color_counter >= threshold:
                return current_color
                
            # 4. 增加微小的延时，避免 CPU 占用过高且给传感器反应时间
            time.sleep(delay)

            

        



       
        

       
        
