

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

    print("任务3启动：首先前进4cm以越过起始线。")
    robot.drive(0.04) # 前进4cm
    time.sleep(1) # 等待移动完成
    robot.stop()
    print("已越过起始线。")

    # 这是一个新的、更强大的导航函数，能够处理交叉路口
    def go_to_next_node(robot, current_node, next_node, controller, velocity):
        """
        导航机器人从一个节点到下一个节点。
        - 如果当前节点是红色（交叉口），则执行特殊逻辑（前进、旋转、定位）。
        - 然后，沿黑线循迹，直到到达目标节点。
        """
        current_node_color = color_dict[current_node]
        target_color = color_dict[next_node]

        print(f"准备从 {current_node}({current_node_color}) 前往 {next_node}({target_color})")

        # 步骤 1: 处理在当前节点的出发逻辑, 特别是红色交叉口
        if current_node_color == "Red":
            print("当前节点是红色交叉口，执行特殊导航...")
            
            # 1. 向前行驶20cm，进入交叉口中心，以便旋转
            print("  - 前进20cm")
            robot.drive(0.2)
            # FMLRobot.drive() 是非阻塞的，需要等待它完成。
            # 由于没有编码器反馈，我们根据经验使用 time.sleep()。1.5秒对于20cm是一个合理的估计。
            time.sleep(1.5)
            robot.stop()

            # 2. 缓慢旋转，用颜色传感器寻找指向下一个目标节点的颜色路径
            print(f"  - 旋转以寻找路径颜色: {target_color}")
            rotation_speed_dps = 45  # 较慢的旋转速度以便检测
            robot.BP.set_motor_dps(robot.left_motor, rotation_speed_dps)
            robot.BP.set_motor_dps(robot.right_motor, -rotation_speed_dps)

            while True:
                # 同时使用左右两个传感器以提高稳定性
                color_l = robot.get_color_left()
                color_r = robot.get_color_right()
                if color_l == target_color or color_r == target_color:
                    print(f"  - 找到 {target_color} 路径标记，停止旋转。")
                    robot.stop()
                    break # 找到了正确的方向
                time.sleep(0.02) # 短暂延时，避免CPU占用过高

        # 步骤 2: 沿黑线循迹，直到到达目标节点
        print(f"开始沿黑线行驶，直到看见目标颜色: {target_color}")
        
        # 在开始循迹前，先短暂前进，确保离开当前节点的颜色区域
        # robot.BP.set_motor_dps(robot.left_motor, velocity)
        # robot.BP.set_motor_dps(robot.right_motor, velocity)
        # time.sleep(1.5)
        robot.drive(0.08)

        while True:
            # 检查是否已到达目标
            color_l = robot.get_color_left()
            color_r = robot.get_color_right()
            if color_l == target_color or color_r == target_color:
                print(f"成功到达节点 {next_node} (颜色: {target_color})")
                robot.stop()
                break  # 到达目标，结束本次循迹

            # 执行PID循迹逻辑
            try:
                current_sensor_value = robot.BP.get_sensor(robot.right_sensor)
                u = controller.get_u(current_sensor_value)
                
                # 限制最大速度差，防止速度过快
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

    # 4. 执行第一段导航，前往存放点
    for i in range(len(path_to_storage) - 1):
        current_node = path_to_storage[i]
        next_node = path_to_storage[i+1]
        go_to_next_node(robot, current_node, next_node, controller, velocity)
        time.sleep(0.5) # 每个节点停顿一下，增加稳定性

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
        go_to_next_node(robot, current_node, next_node, controller, velocity)
        time.sleep(0.5)

    # 8. 任务结束
    print(f"========== 成功到达离场节点 {exit_node}，任务 3 结束 ==========")
    robot.stop()