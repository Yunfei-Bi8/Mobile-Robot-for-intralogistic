import sys
sys.path.append("..")
sys.path.append(".")
from FMLRobot import FMLRobot
from FMLController import PIController
from FMLCamera import FMLCamera
from FMLMqtt import FMLMqtt
import time

AVAILABLE_FORMS = ["Circle", "Rectangle", "Triangle", "Ellipse"]

def doTask(robot : FMLRobot, mqtt : FMLMqtt, camera: FMLCamera):
    
    # 提取通用的“循迹直到看到指定颜色”的函数 (和 aufgabe 3 类似)
    def follow_line_until_color(robot, target_color, controller, velocity):
        print(f"开始寻线，寻找颜色: {target_color}...")
        
        # 强制起步盲开 0.5 秒，防止被当前脚下的同色色块卡死
        robot.BP.set_motor_dps(robot.left_motor, velocity)
        robot.BP.set_motor_dps(robot.right_motor, velocity)
        time.sleep(0.5) 
        
        while True:
            # 检测是否到达目标颜色
            current_color = robot.get_color_left()
            if current_color == target_color:
                print(f"已到达目标颜色: {target_color}，停车。")
                robot.stop()
                break

            # 执行标准的 PI 循迹逻辑
            try:
                current_sensor_value = robot.BP.get_sensor(robot.right_sensor)
                u = controller.get_u(current_sensor_value)
                
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
                pass # 忽略传感器偶尔的读取失败
                
            time.sleep(0.01)

    # ================= Task 4 主逻辑 =================

    # 1. 初始化控制器和速度
    controller = PIController(kp=1.2, ki=0.0, target_value=50.0)
    velocity = 150

    # 2. 循迹前往蓝点 (Blue marker)
    print("========== Task 4: 前往交互点 ==========")
    # 【加上这行防呆设计】确保 MQTT 已连接
    if not mqtt.is_connected:
        print("正在连接 MQTT 服务器...")
        mqtt.connect()
    follow_line_until_color(robot, "Blue", controller, velocity)

    # 3. 发送到达通知 (MQTT Publish)
    arrival_msg = "Arrived at blue marker. Waiting for container."
    print(f"发送 MQTT 消息: '{arrival_msg}'")
    mqtt.publish(arrival_msg)

    # 4. 等待工人的回复信息 (MQTT Subscribe & Wait)
    print("正在等待工人回复包装形状信息...")
    
    # 注意：确保在 challenge.py 或主程序启动时，mqtt.connect() 已经被调用过
    received_shape = mqtt.read_message()
    
    print(f"收到工人的 MQTT 回复: {received_shape}")

    # 验证收到的形状是否在允许的列表中
    if any(form.lower() in received_shape.lower() for form in AVAILABLE_FORMS):
        print(f"确认包装形状有效。准备继续前进...")
    else:
        print(f"警告：收到的形状 '{received_shape}' 不在标准列表内，但仍继续任务。")

    # 5. 获得信息后，继续循迹前往最终红点 (Red marker)
    print("========== 获得信息，继续前往终点 ==========")
    follow_line_until_color(robot, "Red", controller, velocity)

    print("========== Task 4 顺利完成 ==========")