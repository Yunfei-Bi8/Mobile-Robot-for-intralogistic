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
line_controller = PIController(kp=1.2,ki=0.0,target_value=50.0)  
velocity = 150 # 新增小车的基础循迹速度

done = False
current_task_number = -1

with FMLRobot() as robot:
    while not done:
        # reset current taks number
        current_task_number = -1
        
        # TODO add code to read in the task number somehow and drive between the tasks
        ##update in challenge1
        # --- 新增的检测与循迹逻辑开始 ---
        color_left = robot.get_color_left()
        
        if color_left == "Red":
            print("检测到红色起点标记，停车...")
            robot.stop()

            # 左转90度以扫描任务二维码
            print("左转90度扫描任务二维码...")
            robot.turn(90)
            time.sleep(0.5)

            # 持续扫描，直到成功读取一个有效的任务编号
            while True:
                print("正在扫描二维码...")
                qr_data = camera.get_barcode()

                if qr_data is not None:
                    try:
                        current_task_number = int(qr_data)
                        print(f"成功读取到任务编号: {current_task_number}")
                        break  # 成功读取，跳出扫描循环
                    except ValueError:
                        print(f"二维码内容无效 '{qr_data}'。请出示正确的任务二维码。1秒后重试...")
                        # time.sleep(1)
                else:
                    print("未扫描到二维码，请将二维码对准摄像头。1秒后重试...")
                    # time.sleep(1)
            
            # 只有成功扫描后，才会执行到这一步
            print("右转90度准备执行任务...")
            robot.turn(-90)
            time.sleep(0.5)
                
        else:
            # 如果没看到红块，执行默认的PID循迹
            try:
                current_sensor_value = robot.BP.get_sensor(robot.right_sensor)
                u = line_controller.get_u(current_sensor_value)
                
                # 限制最大速度差
                if velocity + abs(u) > 500:
                    u = (500 - velocity) if u >= 0 else (velocity - 500)

                # 设置左右轮速度
                if u >= 0:
                    robot.BP.set_motor_dps(robot.right_motor, velocity - abs(u))
                    robot.BP.set_motor_dps(robot.left_motor, velocity + abs(u))
                else:
                    robot.BP.set_motor_dps(robot.right_motor, velocity + abs(u))
                    robot.BP.set_motor_dps(robot.left_motor, velocity - abs(u))
            except Exception:
                pass # 忽略传感器读取失败
                
            time.sleep(0.01)
            # continue # 循迹中，跳过任务分发代码
        # --- 新增的检测与循迹逻辑结束 ---


        if current_task_number == 1:
            aufgabe_1.doTask(robot,mqtt,camera)
        if current_task_number == 2:
            aufgabe_2.doTask(robot,mqtt,camera)
        if current_task_number == 3:
            aufgabe_3.doTask(robot,mqtt,camera)
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
        
