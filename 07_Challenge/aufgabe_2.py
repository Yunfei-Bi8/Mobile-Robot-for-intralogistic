import sys
import time
sys.path.append("..")
sys.path.append(".")
from FMLRobot import FMLRobot
from FMLCamera import FMLCamera
from FMLMqtt import FMLMqtt
from FMLController import PIController

def doTask(robot: FMLRobot, mqtt: FMLMqtt, camera: FMLCamera):
    """
    任务2：按条形码分拣容器。
    1. 等待并扫描一个"注册"条形码。
    2. 沿黑线行驶，寻找蓝色标记点。
    3. 在蓝色标记点，扫描容器条形码并与注册条形码比对。
    4. 如果匹配，则执行升降叉动作。
    5. 任务在检测到下一个红色标记点时结束。
    """
    print("--- 启动 Task 2: 按条形码分拣容器 ---")
    robot.stop()

    # 向前行驶5cm以越过红色方块
    print("向前行驶5cm以越过红色方块...")
    robot.drive(0.05) # 5cm

    # ==========================================
    # 阶段 1: 等待并扫描 "register" 条形码
    # ==========================================
    registered_barcode = None
    print("请将“注册条形码” (register barcode) 展示在摄像头前...")
    while registered_barcode is None:
        registered_barcode = camera.get_barcode()
        if registered_barcode is None:
            print("未检测到条形码，请对准摄像头...")
            time.sleep(0.5)

    print(f"注册条形码已记录: [{registered_barcode}]")
    print("2秒后开始沿黑线行驶，寻找蓝色标记...")
    time.sleep(2.0)

    # ==========================================
    # 阶段 2: 沿线行驶并根据颜色标记执行操作
    # ==========================================
    # 循迹参数 (与challenge.py保持一致)
    line_controller = PIController(kp=1.2, ki=0.0, target_value=50.0)  
    velocity = 150
    fork_action_done = False

    while True:
        # 优先检查颜色标记
        color_left = robot.get_color_left()

        # 结束条件: 如果检测到红色标记, 任务结束
        if color_left == "Red":
            print("检测到下一个任务的红色标记，Task 2 结束。")
            robot.stop()
            break  # 退出while循环, 从而结束doTask函数

        # 行为条件: 如果检测到蓝色标记
        if color_left == "Blue" and not fork_action_done:
            print("检测到蓝色标记，停车并准备扫描容器...")
            robot.stop()

            # 新增逻辑: 右转90度以面向容器
            print("右转90度...")
            robot.turn(-90)
            time.sleep(0.5) # 转弯后短暂稳定

            # 扫描容器上的条形码，直到成功
            while True:
                container_barcode = camera.get_barcode()
                if container_barcode is not None:
                    print(f"扫描到容器条形码: [{container_barcode}]")
                    if container_barcode == registered_barcode:
                        print("条形码匹配！执行升降叉操作。")
                        ##let the agv move 8cm forward to get nearer to the good
                        robot.drive(0.08)
                        robot.lift_fork()
                        time.sleep(1.0)
                        robot.drop_fork()
                        print("操作完成。")
                        fork_action_done=True
                    else:
                        print("条形码不匹配，忽略此容器。")
                    break  # 成功扫描或不匹配都退出循环
                else:
                    print("未能在容器位置扫描到条形码，0.5秒后重试...")
                    time.sleep(0.5)

            # 左转90度以返回主线路
            print("左转90度以返回主线路...")
            robot.turn(90)

            # 向前行驶5cm以越过蓝色方块
            print("向前行驶5cm以越过蓝色方块...")
            robot.drive(0.05)
            
            print("继续沿黑线行驶...")
            # 处理完蓝色标记后，循环将继续，机器人会重新开始循迹

        # 默认行为: 循迹 (如果没有检测到特殊颜色标记)
        try:
            current_sensor_value = robot.BP.get_sensor(robot.right_sensor)
            u = line_controller.get_u(current_sensor_value)
            
            # 限制速度，防止电机过载
            if velocity + abs(u) > 500:
                u = (500 - velocity) if u >= 0 else (velocity - 500)

            # 根据u的值调整左右轮速度 (这段逻辑与challenge.py中一致)
            if u >= 0:
                robot.BP.set_motor_dps(robot.right_motor, velocity - abs(u))
                robot.BP.set_motor_dps(robot.left_motor, velocity + abs(u))
            else:
                robot.BP.set_motor_dps(robot.right_motor, velocity + abs(u))
                robot.BP.set_motor_dps(robot.left_motor, velocity - abs(u))
        except Exception:
            # 忽略偶尔的传感器读取失败
            pass
            
        time.sleep(0.01)

    print("--- Task 2 完成 ---")
