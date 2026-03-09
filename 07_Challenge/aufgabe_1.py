# # import sys
# # sys.path.append("..")
# # sys.path.append(".")
# # from FMLRobot import FMLRobot
# # from FMLCamera import FMLCamera
# # from FMLMqtt import FMLMqtt
# # import time

# # def doTask(robot : FMLRobot,mqtt : FMLMqtt,camera: FMLCamera):
# #     pass

# import sys
# import time
# sys.path.append("..")
# sys.path.append(".")
# from FMLRobot import FMLRobot
# from FMLCamera import FMLCamera
# from FMLMqtt import FMLMqtt
# from FMLController import PIController

# def doTask(robot: FMLRobot, mqtt: FMLMqtt, camera: FMLCamera):
#     print("--- 启动 Task 1: 工厂大门前的红绿灯 ---")
    
#     # 确保小车初始状态是停止的
#     robot.stop()
    
#     # ==========================================
#     # 阶段 1：死循环等待绿灯牌子
#     # ==========================================
#     print("等待绿灯指示牌...")
#     while True:
#         # 读取左侧颜色传感器的值
#         color_left = robot.get_color_left()
        
#         if color_left == "Green":
#             print("检测到绿色牌子！准备出发。")
#             break # 看到绿色，跳出等待循环，进入下一个阶段
        
#         # 短暂休眠，防止死循环过度占用 CPU 资源
#         time.sleep(0.1) 


#     # ==========================================
#     # 阶段 2：绿灯亮起，开始循迹前进
#     # ==========================================
#     # 初始化循迹相关的参数
#     # target_value 是黑线和白底的反射率中间值，需根据实际场地光线测试（通常在 40-60 之间）
#     target_light_value = 50 
#     controller = PIController(kp=1.5, ki=0.0, target_value=target_light_value)
#     velocity = 150 # 设置小车的基础行驶速度

#     print("绿灯已触发，开始沿着黑线前进...")
    
#     # 记录开始行驶的时间
#     start_time = time.time()
    
#     # 这里我们设置让小车循迹行驶一段特定的时间（例如 4 秒）以到达下一个任务点
#     # 你可以根据场地中 Task 1 到 Task 2 的实际距离来调整这个时间
#     while time.time() - start_time < 4.0: 
#         try:
#             # 读取右侧光电传感器（循迹传感器）的值
#             current_sensor_value = robot.BP.get_sensor(robot.right_sensor)
#         except Exception as e:
#             # 如果传感器偶尔读取失败，跳过本次循环，防止程序崩溃
#             continue

#         # 使用 PI 控制器计算转向修正量 u
#         u = controller.get_u(current_sensor_value)

#         # 限制转速差，防止电机过载或超出阈值 (500)
#         if velocity + abs(u) > 500:
#             if u >= 0:
#                 u = 500 - velocity
#             else:
#                 u = velocity - 500

#         # 根据 u 的正负来调整左右轮的速度，实现沿线行驶
#         if u >= 0:
#             robot.BP.set_motor_dps(robot.right_motor, velocity - abs(u))
#             robot.BP.set_motor_dps(robot.left_motor, velocity + abs(u))
#         else:
#             robot.BP.set_motor_dps(robot.right_motor, velocity + abs(u))
#             robot.BP.set_motor_dps(robot.left_motor, velocity - abs(u))
        
#         time.sleep(0.01)

#     # 行驶结束，停车并交接给下一个 Task
#     robot.stop()
#     print("--- Task 1 完成，小车已到达位置 2 ---")


# import sys
# sys.path.append("..")
# sys.path.append(".")
# from FMLRobot import FMLRobot
# from FMLCamera import FMLCamera
# from FMLMqtt import FMLMqtt
# import time

# def doTask(robot : FMLRobot,mqtt : FMLMqtt,camera: FMLCamera):
#     pass

import sys
import time
sys.path.append("..")
sys.path.append(".")
from FMLRobot import FMLRobot
from FMLCamera import FMLCamera
from FMLMqtt import FMLMqtt
from FMLController import PIController

def doTask(robot: FMLRobot, mqtt: FMLMqtt, camera: FMLCamera):
    print("--- 启动 Task 1: 工厂大门前的红绿灯 ---")
    
    # 确保小车初始状态是停止的
    robot.stop()
    
    # ==========================================
    # 阶段 1：死循环等待绿灯牌子
    # ==========================================
    print("等待绿灯指示牌...")
    # 定义绿灯检测的阈值。如果画面中绿色像素的占比超过2%，我们就认为检测到了绿灯。
    # 这个值可能需要根据实际情况微调。
    GREEN_THRESHOLD_PERCENTAGE = 2.0 

    while True:
        # 从摄像头获取绿色像素的百分比
        green_percentage = camera.get_green_percentage()
        # 打印当前值，方便调试
        print(f"当前画面绿色占比: {green_percentage:.2f}%")
        
        # 如果检测到的绿色占比超过阈值
        if green_percentage > GREEN_THRESHOLD_PERCENTAGE:
            print(f"检测到绿色！(占比 > {GREEN_THRESHOLD_PERCENTAGE}%)，准备出发。")
            break # 识别到绿色，跳出等待循环
        
        # 短暂休眠，以降低CPU占用率（摄像头处理比简单传感器更耗时）
        time.sleep(0.5) 



    # ==========================================
    # 阶段 2：绿灯亮起，开始循迹前进
    # ==========================================
    # 初始化循迹相关的参数
    # target_value 是黑线和白底的反射率中间值，需根据实际场地光线测试（通常在 40-60 之间）
    target_light_value = 50 
    controller = PIController(kp=1.2, ki=0.0, target_value=target_light_value)
    velocity = 150 # 设置小车的基础行驶速度

    print("绿灯已触发，开始沿着黑线前进...")
    
    # 记录开始行驶的时间
    start_time = time.time()
    
    # 这里我们设置让小车循迹行驶一段特定的时间（例如 4 秒）以到达下一个任务点
    # 你可以根据场地中 Task 1 到 Task 2 的实际距离来调整这个时间
    while time.time() - start_time < 4.0: 
        try:
            # 读取右侧光电传感器（循迹传感器）的值
            current_sensor_value = robot.BP.get_sensor(robot.right_sensor)
        except Exception as e:
            # 如果传感器偶尔读取失败，跳过本次循环，防止程序崩溃
            continue

        # 使用 PI 控制器计算转向修正量 u
        u = controller.get_u(current_sensor_value)

        # 限制转速差，防止电机过载或超出阈值 (500)
        if velocity + abs(u) > 500:
            if u >= 0:
                u = 500 - velocity
            else:
                u = velocity - 500

        # 根据 u 的正负来调整左右轮的速度，实现沿线行驶
        if u >= 0:
            robot.BP.set_motor_dps(robot.right_motor, velocity - abs(u))
            robot.BP.set_motor_dps(robot.left_motor, velocity + abs(u))
        else:
            robot.BP.set_motor_dps(robot.right_motor, velocity + abs(u))
            robot.BP.set_motor_dps(robot.left_motor, velocity - abs(u))
        
        time.sleep(0.01)

    # 行驶结束，停车并交接给下一个 Task
    robot.stop()
    print("--- Task 1 完成，小车已到达位置 2 ---")