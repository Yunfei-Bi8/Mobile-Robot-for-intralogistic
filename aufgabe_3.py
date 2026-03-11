from operator import ne
import sys
sys.path.append("..")
sys.path.append(".")
from FMLRobot import FMLRobot
from FMLController import PIController
from FMLCamera import FMLCamera
from FMLMqtt import FMLMqtt
from dijkstra import dijkstra
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

def navigate(robot, start_node, end_node, route, controller):
    index = 0
    current_node = start_node
    # This while should drive to the center of the node
    # and scan the colors until the correct color is detected
    while (current_node is not end_node):
        # Drive to the center of the node
        robot.drive(0.2)
        current_node = route[index]
        index = index + 1
        next_node = route[index]
        next_color = color_dict[route[index]]
        print ("Next node", next_node)
        print ("Next color", next_color)
        color = robot.get_color_left()
        while (color is not next_color):
            # Turn around until right color is found
            robot.turn(-15)
            color = robot.get_color_left()
            print ("Color found is", color)
        print ("Color reached")
        current_node = next_node
        robot.drive(0.05)
        robot.follower_line(velocity=150,controller=controller, stop_color = "Red")


def navigate_from_storage_to_exit(robot, start_node, end_node, route, controller):
    index = 0
    current_node = start_node
    # This while should drive to the center of the node
    # and scan the colors until the correct color is detected
    #this flag is to make sure that only in the first interation of the loop, the robot will not move forward for 20cm,
    #because here when we go back from the storage point, we are already at the centre point and we are ready for rotating to find the right color
    #but for the other iter. of the loop, we have to move forward for 20 cm to reach the centre
    flag_for_moving_forward=False 
    while (current_node is not end_node):
        if flag_for_moving_forward:
            robot.drive(0.2) 
        flag_for_moving_forward= True
        
        current_node = route[index]
        index = index + 1
        next_node = route[index]
        next_color = color_dict[route[index]]
        print ("Next node", next_node)
        print ("Next color", next_color)
        color = robot.get_color_left()
        while (color is not next_color):
            # Turn around until right color is found
            robot.turn(-15)
            color = robot.get_color_left()
            print ("Color found is", color)
        print ("Color reached")
        current_node = next_node
        robot.drive(0.05)
        robot.follower_line(velocity=150,controller=controller, stop_color = "Red")

def doTask(robot : FMLRobot,mqtt : FMLMqtt,camera: FMLCamera, end_node):
    start_node = "a"
    pi_controller = PIController(kp=1.2,ki=0.0,target_value=50.0)
    # Follow line until red mark
    robot.follower_line(velocity=200,controller=pi_controller, stop_color = "Red")
    # Get Dijkstra route
    route = dijkstra(graph,start_node,end_node)
    print ("Route is:", route)
    navigate(robot, start_node, end_node, route, pi_controller)
    # Here the end of the maze is founded 
    
    # Now move forward to the center of the node and look for the green color
    robot.drive(0.2) #here we are at the centre
    print("move forward for 20 cm to reach the centre")
    #now we rotate to find the green mark(the storage place for dropping good)
    color=robot.get_color_left()
    while(color!="Green"):
        # Turn around until right color is found
            robot.turn(-15)
            color = robot.get_color_left()
            print ("Color found is", color)
    print("found green mark and ready to move forward to drop the good")
    robot.drive(0.09) #now we move forward further to the green mark to drop our good
    print("move forward from centre for 9 cm")
    # robot.drop_fork()#we drop the good
    robot.drive(-0.09)#we move back to the centre again
    print("move backward to centre")
    # robot.lift_fork()#we lift the fork again

    # robot.drive(-0.2)#here we have to move backward for 20cm. to the red mark
    #because in the navigate func., the robot still move 20 cm forward to the centre

   
    
    # Here find the path to the exit
    start_node = end_node
    end_node = "n"
    print ("Current node", start_node)
    route_to_exit = dijkstra(graph, start_node, end_node)
    navigate_from_storage_to_exit(robot, start_node, end_node, route_to_exit, pi_controller)#navigate to the exit node

    print ("Task 3 finished")
    robot.stop()
    time.sleep(10)




