# 

from picamera2 import Picamera2
import numpy as np
import cv2
import pyzbar.pyzbar as pyzbar
import time
import cv2.aruco as aruco

class FMLCamera:

    def __init__(self):
        self.resolution = (800, 400) # rows x columns
        self._pi_camera = Picamera2()
        # Create and apply a configuration
        config = self._pi_camera.create_preview_configuration(main={"size": self.resolution, "format": "BGR888"})
        self._pi_camera.configure(config)
        self._pi_camera.start()
        # Allow camera to warm up
        time.sleep(2)

    
    # Destructor (gets called once the object is destroyed)
    def __del__(self):
        # Frees ressources connected to the camera
        if self._pi_camera.started:
            self._pi_camera.stop()
        self._pi_camera.close() 
    
    # Return a BGR image array
    def get_image_array(self):
        # The format is already BGR888 as configured in __init__
        frame = self._pi_camera.capture_array("main")
        return frame

    # saves a image to disk - probably usefull for the shape recognition.
    def save_to_disk(self, path_to_image):
        self._pi_camera.capture(path_to_image)

    # ... (other methods remain the same) ...


    ##update in challenge1
    def get_barcode(self):
        """
        捕获图像并尝试解析二维码/条形码。
        如果解析成功，返回解码后的字符串；否则返回 None。
        """
        # 获取当前图像帧
        image = self.get_image_array()
        
        # 将图像转换为灰度图，以提高 pyzbar 的识别率
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # 寻找并解码图像中的条形码/二维码
        decoded_objects = pyzbar.decode(gray)
        
        for obj in decoded_objects:
            # 提取并解码二维码内的数据
            qr_data = obj.data.decode('utf-8')
            print(f"检测到二维码数据: {qr_data}")
            return qr_data
            
        return None
               
    # def get_green_percentage(self):
    #     pass
    ##update in challenge1
    def get_green_percentage(self):
        """
        Calculates the percentage of green pixels in the camera's view.
        This is useful for detecting things like a green traffic light.

        Returns:
            float: The percentage of green pixels in the total image area (0-100).
        """
        # 1. Get an image from the camera
        image = self.get_image_array()

        # 2. Convert the BGR image to the HSV color space
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # 3. Define the range for the color green in HSV.
        # These values might need adjustment depending on the specific shade of green
        # and the lighting conditions of the environment.
        # Format is [Hue, Saturation, Value]
        lower_green = np.array([35, 80, 80])
        upper_green = np.array([85, 255, 255])

        # 4. Create a binary mask where green pixels are white and others are black
        mask = cv2.inRange(hsv_image, lower_green, upper_green)

        # 5. Calculate the percentage of green pixels
        total_pixels = image.shape[0] * image.shape[1]
        if total_pixels == 0:
            return 0.0 # Avoid division by zero

        green_pixels = np.count_nonzero(mask)
        
        green_percentage = (green_pixels / total_pixels) * 100
            
        return green_percentage

    def get_shapes_on_image(self,path_to_image):
        pass

    def get_qr_position(self):
        pass

    def get_aruco_offset(self, target_id=None):
        """
        Detects ArUco markers and returns the horizontal offset of a specific marker
        from the center of the image.
        A positive offset means the marker is to the right of the robot.
        A negative offset means the marker is to the left.
        Returns None if the specified marker is not detected.
        """
        image = self.get_image_array()
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Use the classic OpenCV Aruco API for broader compatibility
        aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_100)
        parameters = aruco.DetectorParameters_create()
        corners, ids, _ = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
        print("ID",ids)

        if ids is not None:
            

        # for i, marker_id in enumerate(ids.flatten()):
        #     if target_id is None or marker_id == target_id:
        #         marker_corners=corners[i][0]
        #         center_x=np.mean(marker_corners[:,0])
        #         image_center_x=self.resolution[0]/2
        #         offset=center_x-image_center_x
        #         print(f"ArUco ID {marker_id} detected, offset:{offset:.1f}px")
        #         return offset
            for i, marker_id in enumerate(ids.flatten()):
                # --- 添加这行 Debug 代码 ---
                print(f"DEBUG: 看到的 marker_id = {marker_id} (类型: {type(marker_id)}), 寻找的 target_id = {target_id} (类型: {type(target_id)})")
                
                if target_id is None or marker_id == target_id:
                    marker_corners = corners[i][0]
                    center_x = np.mean(marker_corners[:,0])
                    image_center_x = self.resolution[0] / 2
                    offset = center_x - image_center_x
                    print(f"ArUco ID {marker_id} detected, offset:{offset:.1f}px")
                    return offset
            
        return 0

    # def get_aruco_offset(self, target_id=None):
    #     """
    #     Detects ArUco markers and returns the horizontal offset of a specific marker
    #     from the center of the image.
    #     A positive offset means the marker is to the right of the robot.
    #     A negative offset means the marker is to the left.
    #     Returns None if the specified marker is not detected.
    #     """
    #     image = self.get_image_array()
    #     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    #     # Use the classic OpenCV Aruco API for broader compatibility
    #     aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_100)
    #     parameters = cv2.aruco.DetectorParameters_create()
    #     corners, ids, _ = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

    #     if ids is not None and target_id in ids:
    #         # Find the index of the target_id
    #         target_index = np.where(ids == target_id)[0][0]
            
    #         # Get the corners of the target marker
    #         marker_corners = corners[target_index][0]
            
    #         # Calculate the horizontal center of the marker
    #         marker_center_x = np.mean(marker_corners[:, 0])
            
    #         # The horizontal center of the camera image
    #         camera_center_x = self.resolution[0] / 2.0
            
    #         offset = marker_center_x - camera_center_x
            
    #         # Adding print statements for debugging
    #         print(f"Detected ArUco ID: {target_id} at center {marker_center_x:.2f}, offset: {offset:.2f}")
            
    #         return offset
        
    #     else:
    #         # Optional: print detected IDs if the target is not among them
    #         if ids is not None:
    #             print(f"Target ID {target_id} not found. Detected IDs: {ids.flatten()}")
    #         else:
    #             print("No ArUco markers detected.")
    #         return None
