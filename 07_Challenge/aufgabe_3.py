from operator import ne
import sys
sys.path.append("..")
sys.path.append(".")
from FMLRobot import FMLRobot
from FMLController import PIController
from FMLCamera import FMLCamera
from FMLMqtt import FMLMqtt
import dijkstra
import time

graph = {"a": {"b": 2, "d": 5, "f": 6},
          "b": {"c": 3, "e": 2},
          "c": {"g": 8, "e": 1},
          "d": {"e": 1, "h": 10},
          "e": {"g": 10, "h": 10},
          "f": {"d": 2, "i": 4},
          "g": {"j": 8},
          "h": {"j": 6, "k": 6},
          "i": {"h": 7, "l": 4},
          "j": {"n": 5, "k": 7},
          "k": {"i": 7, "n": 9},
          "l": {"m": 9},
          "m": {"k": 1},
          "n": {"o": 1},
          "o": {},
}

color_dict = {'a': "Blue", 'b': "Red", 'c': "Blue", 'd': "Blue", 'e': "Red",
                  'f': "Yellow", 'g': "Blue", 'h': "Yellow", 'i': "Red", 'j': "Red",
                  'k': "Blue", 'l': "Blue", 'm': "Red", 'n': "Yellow", 'o': "Red"}

def doTask(robot : FMLRobot, mqtt : FMLMqtt, camera: FMLCamera):
    
    # 这是一个修复后的、可运行的循迹到指定颜色的内部函数
    def follow_line_until_color(robot, target_color, controller, velocity):
        print(f"开始寻找颜色: {target_color}...")
        
        # 【重要优化】：起步时先强制往前开一小段（0.5秒）。
        # 防止小车还在当前节点（比如 a 点是蓝色），而下一个目标也是蓝色时，小车原地不动直接判断到达。
        robot.BP.set_motor_dps(robot.left_motor, velocity)
        robot.BP.set_motor_dps(robot.right_motor, velocity)
        time.sleep(0.5) 
        
        while True:
            # 1. 检测是否到达目标颜色
            current_color = robot.get_color_left()
            if current_color == target_color:
                print(f"成功检测到目标颜色: {target_color}，停车。")
                robot.stop()
                
                # 如果你的小车颜色传感器在车头，停车时可能货叉还没到位置。
                # 如果需要，可以取消下面这行注释，让小车识别到颜色后再往前稍微开一点对准节点。
                # robot.drive(0.05)  
                break

            # 2. 如果没到目标，执行标准的 PID 循迹逻辑 (提取自 challenge.py)
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

    # ================= 任务主逻辑开始 =================
    
    # 1. 初始节点设置
    start_node = 'a'
    target_storage = 'k'  # 你可以在这里改成 'g', 'i', 'k' 或 'l'
    exit_node = 'n'
    
    # 2. 初始化已被证明有效的 PI 控制器和基础速度
    controller = PIController(kp=1.2, ki=0.0, target_value=50.0)
    velocity = 150

    # 3. 计算去存放点(k)的路径
    print(f"计算从 {start_node} 到 {target_storage} 的路径...")
    path_to_storage = dijkstra.dijkstra(graph, start_node, target_storage)
    print(f"路径为: {path_to_storage}")

    # 4. 执行第一段导航
    for i in range(len(path_to_storage) - 1):
        current_node = path_to_storage[i]
        next_node = path_to_storage[i+1]
        target_color = color_dict[next_node]
        
        print(f"-> 正在从节点 {current_node} 前往节点 {next_node}")
        follow_line_until_color(robot, target_color, controller, velocity)
        time.sleep(0.5) # 每个节点停顿一下，防止姿态不稳

    # 5. 到达存放点，执行卸货
    print(f"========== 到达存放节点 {target_storage} ==========")
    robot.stop()
    print("正在卸货 (放下货叉)...")
    robot.drop_fork()
    time.sleep(1) # 卸货后等待1秒

    # 6. 计算离开去(n)的路径
    print(f"计算从 {target_storage} 到离场点 {exit_node} 的路径...")
    path_to_exit = dijkstra.dijkstra(graph, target_storage, exit_node)
    print(f"离开路径为: {path_to_exit}")
    
    # 7. 执行离开导航
    for i in range(len(path_to_exit) - 1):
        current_node = path_to_exit[i]
        next_node = path_to_exit[i+1]
        target_color = color_dict[next_node]
        
        print(f"-> 正在从节点 {current_node} 前往节点 {next_node}")
        follow_line_until_color(robot, target_color, controller, velocity)
        time.sleep(0.5)

    # 8. 任务结束
    print(f"========== 成功到达离场节点 {exit_node}，任务 3 结束 ==========")
    robot.stop()