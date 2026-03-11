import sys
sys.path.append("..")
sys.path.append(".")
from FMLRobot import FMLRobot
from FMLCamera import FMLCamera
from FMLMqtt import FMLMqtt
from FMLController import PIController
import time 
import aufgabe_1 
import aufgabe_2
import aufgabe_3 
import aufgabe_4 
import aufgabe_5 
import aufgabe_6 
import aufgabe_7 
import aufgabe_8 


camera = FMLCamera()
mqtt = FMLMqtt("mqttBroker","gruppeX/robot")

##update in challenge 1
# line_controller = PIController(0,0.00,0)

pi_controller = PIController(kp=1.2,ki=0.0,target_value=50.0)
velocity = 150 # 新增小车的基础循迹速度

done = False
current_task_number = 3

with FMLRobot() as robot:
    while not done:
        # reset current taks number
        robot.follower_line(velocity=200,controller=pi_controller, stop_color = "Red")
        robot.turn(90)
        time.sleep(0.5)
        code_read = False
        while (code_read):
            current_task_number = camera.get_barcode()
            print (current_task_number)
        print ("Current task:", current_task_number)
        robot.turn (-90)
        robot.drive(0.05)
        


        if current_task_number == 1:
            aufgabe_1.doTask(robot,mqtt,camera)
        if current_task_number == 2:
            aufgabe_2.doTask(robot,mqtt,camera)
        if current_task_number == 3:
            end_node = "g"
            aufgabe_3.doTask(robot, mqtt, camera, end_node)
        if current_task_number == 4:
            aufgabe_4.doTask(robot,mqtt,camera)
        if current_task_number == 5:
            aufgabe_5.doTask(robot,mqtt,camera)
        if current_task_number == 6:
            aufgabe_6.doTask(robot,mqtt,camera)
        if current_task_number == 7:
            aufgabe_7.doTask(robot,mqtt,camera)
        if current_task_number == 8:
            aufgabe_8.doTask(robot,mqtt,camera)
            done = True
        
