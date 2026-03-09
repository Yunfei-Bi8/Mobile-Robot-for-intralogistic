import time
from FMLController import PIController
from map import MAP

def navigate_to_aruco_simple(self, camera, target_id=None, target_distance_cm=10, velocity=150, map_object=None):
        from FMLController import PController
        controller = PController(kp=1.2, target_value=0)
        last_save_time = time.time()
        snapshot_id=0
        
        while True:
            offset = camera.get_aruco_offset(target_id=target_id)
            print("Offset is:",offset)
            front_distance = self.get_distance_front()

            # If the front_distance is less than 10 cm stop,test
            # if front_distance<10:
            # #   self.stop()
            #   print("Too near!")
            #   break
            if front_distance!=-1 and front_distance<target_distance_cm:
                 break

            u = controller.get_u(offset)
            # Limit u to 500
            if velocity + abs(u) > 500:
                if u >= 0:
                    u = 500 - velocity
                else:
                    u = velocity - 500
            # Run motors
            if u >= 0:
                self.BP.set_motor_dps(self.right_motor,velocity - abs(u))
                self.BP.set_motor_dps(self.left_motor,velocity + abs(u))
            else:
                self.BP.set_motor_dps(self.right_motor,velocity + abs(u))
                self.BP.set_motor_dps(self.left_motor,velocity - abs(u))

            self.update_position()

            if map_object is not None:
                 
                current_time = time.time()
                if current_time - last_save_time > 1:
                  map_object.robot_position = (self.position[0] * 10, self.position[1] * 10)
                  filename = f"map.png"
                  map_object.save_map(filename)
                  print(f"Saved {filename}")
                  snapshot_id += 1
                  last_save_time = current_time

            time.sleep(0.01)

        self.stop()

        