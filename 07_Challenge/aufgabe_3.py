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

# 场地节点拓扑图
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

# 节点对应的目标颜色映射
color_dict = {'a': "Blue", 'b': "Red", 'c': "Blue", 'd': "Blue", 'e': "Red",
                  'f': "Yellow", 'g': "Blue", 'h': "Yellow", 'i': "Red", 'j': "Red",
                  'k': "Blue", 'l': "Blue", 'm': "Red", 'n': "Yellow", 'o': "Red"}

# ==========================================
# Task 3 专属配置
# ==========================================
START_NODE = 'a'        # 仓库入口节点
TARGET_STORAGE = 'k'    # 目标存储点 (可在 'g', 'i', 'k', 'l' 中更改)
EXIT_NODE = 'n'         # 离开仓库的出口节点


def navigate_path(robot: FMLRobot, path: list):
    """
    根据给定的节点列表依次导航，执行你要求的状态机逻辑
    """
    controller = PIController(kp=1.2, ki=0.0, target_value=50.0)
    velocity = 150
    flag_spin= False
    color_counter = 0
    
    print(f"开始导航路径: {' -> '.join(path)}")
    
    for i in range(1, len(path)):
        current_node = path[i-1]
        next_node = path[i]
        target_color = color_dict.get(next_node, "None")
        print("next node color",target_color)
        
        print(f"\n>> 正在从 {current_node} 前往 {next_node} (目标颜色: {target_color})")
        
        # ---------------------------------------------------------
        # 步骤 1: PID 沿黑线行驶，直到检测到红色
        # ---------------------------------------------------------
        print("状态: PID 循迹中，等待红色标记...")
        while True:
            # 1. 直接把获取颜色的“方法”传进去（注意：get_color_left 后面不要加括号 ()）
            # 让 debouncing 函数内部去不断调用它读取新颜色
            real_color = robot.debouncing(robot.get_color_left)

            print("current color:", real_color)
            
            # 2. ⚠️ 必须用去抖动后返回的 real_color 来判断，不能用原来的 color
            if real_color == "Red":
                print("【触发】检测到红色！。")
                robot.stop()
                break
                        
            # # 安全机制：障碍物检测 (可选)
            # front_distance = robot.get_distance_front()
            # if front_distance != -1 and front_distance < 15:
            #     print("警告：前方检测到障碍物！停车等待。")
            #     robot.stop()
            #     time.sleep(1) # 可以根据需要调整避障逻辑
            #     continue

            # 基础 PID 循迹
            current_sensor_value = robot.BP.get_sensor(robot.right_sensor)
            u = controller.get_u(current_sensor_value)
                
                # 限制最大速度差
            if velocity + abs(u) > 500:
                    u = (500 - velocity) if u >= 0 else (velocity - 500)

                # 调整左右轮电机速度
            if u >= 0:
                    robot.BP.set_motor_dps(robot.right_motor, velocity - abs(u))
                    robot.BP.set_motor_dps(robot.left_motor, velocity + abs(u))
            else:
                    robot.BP.set_motor_dps(robot.right_motor, velocity + abs(u))
                    robot.BP.set_motor_dps(robot.left_motor, velocity - abs(u))
                
            time.sleep(0.01)
            
        # ---------------------------------------------------------
        # 步骤 2: 向前直行 12cm
        # ---------------------------------------------------------
        print("状态: 驶入路口，向前直行 20cm...")
        robot.drive(0.20)  # drive 接受的是米为单位
        
        # ---------------------------------------------------------
        # 步骤 3: 旋转并不断检测下方颜色，直到匹配 target_color
        # ---------------------------------------------------------
        print(f"状态: 开始旋转，寻找对应节点 {next_node} 的颜色 [{target_color}]...")
        flag_spin= True
        # 开启旋转：一侧电机正转，一侧反转 (这里默认右转扫描，如果场地左转多可以把正负号调换)
        robot.BP.set_motor_dps(robot.left_motor, 100)
        robot.BP.set_motor_dps(robot.right_motor, -100)
        
        while True:
            if robot.get_color_left() == target_color:
                print(f"【触发】匹配到目标颜色 {target_color}！停止旋转。")
                flag_spin= False
                robot.stop()
                current_sensor_value = robot.BP.get_sensor(robot.right_sensor)
                u = controller.get_u(current_sensor_value)
                
                # 限制最大速度差
                if velocity + abs(u) > 500:
                        u = (500 - velocity) if u >= 0 else (velocity - 500)

                    # 调整左右轮电机速度
                if u >= 0:
                        robot.BP.set_motor_dps(robot.right_motor, velocity - abs(u))
                        robot.BP.set_motor_dps(robot.left_motor, velocity + abs(u))
                else:
                        robot.BP.set_motor_dps(robot.right_motor, velocity + abs(u))
                        robot.BP.set_motor_dps(robot.left_motor, velocity - abs(u))

                color=robot.get_color_left()
            
                # 2. ⚠️ 必须用去抖动后返回的 real_color 来判断，不能用原来的 color
                if color == "Red":
                    print("【触发】检测到红色！。")
                    robot.stop()
                    break
                
                    # break
                time.sleep(0.01)
            
        # 循环结束，进入下一次迭代，立刻恢复 PID 循迹
        print("--> 成功对准新路线，准备恢复 PID 循迹。")


def doTask(robot: FMLRobot, mqtt: FMLMqtt = None, camera: FMLCamera = None):
    """
    执行任务 3 的核心逻辑：存储 EC 并离开仓库
    """
    print("\n" + "="*40)
    print(f"--- 任务 3 开始：将 EC 运送至存储点 {TARGET_STORAGE} ---")
    print("="*40)
    
    # 【注意】按照你的要求，仅在任务开始时执行一次：向前移动 8 厘米
    print("初始化: 向前移动 18cm (0.18m)...")
    robot.drive(0.18)
    
    # 1. 规划并导航到存储点
    print(f"\n[阶段 1] 计算从入口 {START_NODE} 到 存储点 {TARGET_STORAGE} 的路径...")
    route_to_storage = dijkstra.dijkstra(graph, START_NODE, TARGET_STORAGE)
    print(route_to_storage)
    navigate_path(robot, route_to_storage)
    
    # 2. 到达存储点区域，寻找绿色标记进行精确卸货
    print(f"\n[阶段 2] 已到达节点 {TARGET_STORAGE} 区域。正在寻找绿色(Green)停车标记...")
    controller = PIController(kp=1.2, ki=0.0, target_value=50.0)
    velocity = 150
    
    while True:
        if robot.get_color_left() == "Green":
            print("检测到绿色标记！停车。")
            robot.stop()
            break
            
        # 维持基础循迹找绿块
        try:
            current_sensor_value = robot.BP.get_sensor(robot.right_sensor)
            u = controller.get_u(current_sensor_value)
            if velocity + abs(u) > 500:
                u = (500 - velocity) if u >= 0 else (velocity - 500)
            if u >= 0:
                robot.BP.set_motor_dps(robot.right_motor, velocity - abs(u))
                robot.BP.set_motor_dps(robot.left_motor, velocity + abs(u))
            else:
                robot.BP.set_motor_dps(robot.right_motor, velocity + abs(u))
                robot.BP.set_motor_dps(robot.left_motor, velocity - abs(u))
        except Exception:
            pass
        time.sleep(0.01)
    
    # 3. 卸货 (放下叉车)
    print("到达存储位置！正在卸载 EC (降下叉车)...")
    # robot.drop_fork()
    time.sleep(1) # 给机构一点运作时间
    # 卸货后可以根据情况选择是否后退一点，避免刮碰
    # robot.drive(-0.05) 
    
    # 4. 规划并导航离开仓库
    print(f"\n[阶段 3] 卸货完成。计算从 {TARGET_STORAGE} 到 出口 {EXIT_NODE} 的路径...")
    route_to_exit = dijkstra.dijkstra(graph, TARGET_STORAGE, EXIT_NODE)
    navigate_path(robot, route_to_exit)
    
    print("\n✅ 任务 3 圆满完成！机器人已到达出口。")
    robot.stop()