# import sys
# sys.path.append("..")
# sys.path.append(".")
# from FMLRobot import FMLRobot
# import math
# import time

# #D1=66.15, D2=68.06, D3=68.88
# #D=67.70
# #ra
# def _init_kinematik(self):
#     self.wheel_radius = 0.0344      # Radius of the wheel in m
#     self.wheel_distance =  0.169525     # Distance of the wheels in m
#     self.wheel_circumference =2*math.pi*0.0344  # Circumference of the wheels in m
#     self.gear_ratio = 24/8          # Gear ratio (calculation from number of teeth)

#     # global position of the robot within the coordinate system [x,y,phi]
#     self.position = [0.0,0.0,0.0]
#     # last encoder values
#     self.encoder_left = self.BP.get_motor_encoder(self.left_motor)
#     self.encoder_right= self.BP.get_motor_encoder(self.right_motor)

# def drive(self, distance):
#     # needed motor rotation to achieve movement
#     delta_angle = 3*self.distance/self.wheel_radius*180/math.pi

#     # add angle to current motor position
#     self.BP.set_motor_position_relative(self.left_motor, delta_angle)
#     self.BP.set_motor_position_relative(self.right_motor, delta_angle)

#     # give motors some time to spin
#     time.sleep(0.5)

#     # read motor velocity until zero --> robot stands still, we can 
#     # return from the function
#     while self.BP.get_motor_status(self.left_motor)[3] != 0:
#         time.sleep(0.02)

# def turn(self, degree):
#     # needed motor rotation to achieve movement
#     deg_right = self.gear_ratio*(self.wheel_distance/(2*self.wheel_radius))*degree
#     deg_left = -deg_right

#     # turning
#     self.BP.set_motor_position_relative(self.left_motor, deg_left)
#     self.BP.set_motor_position_relative(self.right_motor, deg_right)

#     # give motors some time to spin
#     time.sleep(0.5)

#     # read motor velocity until zero --> robot stands still, we can return from the function
#     while self.BP.get_motor_status(self.left_motor)[3] != 0:
#         time.sleep(0.02)

# with FMLRobot() as robot:
#     robot.drive(0.1)
#     robot.drive(-0.1)
#     robot.turn(-90)


# import sys
# sys.path.append("..")
# sys.path.append(".")
# from FMLRobot import FMLRobot
# import time



# with FMLRobot() as robot:
#     robot.drive(0.1)
#     robot.drive(-0.1)
#     robot.turn(-90)
import sys
sys.path.append("..")
sys.path.append(".")
from FMLRobot import FMLRobot
import math
import time

#D1=66.15, D2=68.06, D3=68.88
#D=67.70
#ra
def _init_kinematik(self):
    self.wheel_radius = 0.0344      # Radius of the wheel in m
    # self.wheel_radius = 0.0345 
    self.wheel_distance =  0.1445     # Distance of the wheels in m
    self.wheel_circumference =2*math.pi*0.0344  # Circumference of the wheels in m
    self.gear_ratio = 24/8          # Gear ratio (calculation from number of teeth)

    # global position of the robot within the coordinate system [x,y,phi]
    self.position = [0.0,0.0,0.0]
    # last encoder values
    self.encoder_left = self.BP.get_motor_encoder(self.left_motor)
    self.encoder_right= self.BP.get_motor_encoder(self.right_motor)

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

FMLRobot._init_kinematik = _init_kinematik
FMLRobot.drive = drive
FMLRobot.turn = turn

with FMLRobot() as robot:
    robot.drive(0)
    robot.drive(0)
    robot.turn(360)


