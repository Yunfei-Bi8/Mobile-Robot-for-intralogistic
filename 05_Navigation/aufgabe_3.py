import sys
sys.path.append("..")
sys.path.append(".")
from FMLRobot import FMLRobot
from FMLController import PController
import time

# # with FMLRobot() as robot:
# #     robot.bypass_obstacle()

# with FMLRobot() as robot:
#     dist_controller = PController(kp=1.2, target_value=0.15)   # 15cm
#     robot.bypass_obstacle(velocity=150, controller_distance=dist_controller)


def main():
    with FMLRobot() as robot:
        # 线跟随 controller（按你们之前 Appointment 3 的参数改）
        line_ctrl = PController(kp=1.2, target_value=0.5)  # 这里target_value按你线的定义来

        # 贴障距离 controller：目标 15cm
        dist_ctrl = PController(kp=8.0, target_value=15)

        v = 150
        obstacle_threshold_cm = 15  # 看到障碍的触发阈值（你可以调 10~15）

        while True:
            # 1) 先沿黑线走（这里用“手写循环”，不要直接调用 follower_line() 的死循环版本）
            color = robot.get_color_left()

            # --- 线跟随：你需要用你们 line follower 的“误差量” ---
            # 如果你们是用灰度/光强而不是颜色字符串，就把下面换成对应函数
            # 这里我放一个示意：假设 robot.get_reflection_left() 返回 0~1
            # e = robot.get_reflection_left() - 0.5
            # u = line_ctrl.get_u(robot.get_reflection_left())

            # 如果你现在只有颜色字符串（Black/White），那就先用最简：
            
            # if color == "Black":
            #     robot.BP.set_motor_dps(robot.left_motor, v)
            #     robot.BP.set_motor_dps(robot.right_motor, v)
            # else:
            #     # 找线：轻微转向（按你场地情况调整左右）
            #     robot.BP.set_motor_dps(robot.left_motor, v)
            #     robot.BP.set_motor_dps(robot.right_motor, 0.6 * v)

            # 2) 检测障碍
            d_front = robot.get_distance_front()
            if d_front != -1 and d_front < obstacle_threshold_cm:
                #robot.stop()
                #time.sleep(0.1)

                # 3) 执行 BUG2 绕障（绕完会在看到黑线时停止）
                robot.bypass_obstacle(velocity=v, controller_distance=dist_ctrl,
                                     turn_angle_deg=60, target_lateral_cm=15, line_color="Black")

                # 4) 绕完以后稍微前走一点点，避免立刻又把“黑线”判成停止线
                robot.BP.set_motor_dps(robot.left_motor, v)
                robot.BP.set_motor_dps(robot.right_motor, v)
                time.sleep(0.2)

            time.sleep(0.01)

if __name__ == "__main__":
    main()