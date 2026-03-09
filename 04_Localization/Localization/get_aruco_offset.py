import numpy as np
import cv2

# def get_aruco_offset(self, target_id=None):
#         import cv2.aruco as aruco


#         image = self.get_image_array()
#         gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#         aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_100)
#         parameters = aruco.DetectorParameters_create()

#         corners, ids, _ = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
        
#         if ids is None:
#             return "No ArUco"
        
#         else:
#             print ("ArUco ID", ids, "detected")
#             print ("Corners:", corners)
#             print ("Camera center:", self.resolution[0])

#             ## Calculate the offset between the camera center and the Aruco center in the x axis
#             ## Return the offset calculated
#             ## If the offset is positive it means that the Aruco is to the right of the robot
#             ## If the offset is negative it means that the Aruco is to the left

#         return "No ArUco"

# import numpy as np
# import cv2
# import cv2.aruco

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
        
#         offset = marker_center_x-camera_center_x
        
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
        aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_100)
        parameters = cv2.aruco.DetectorParameters_create()
        corners, ids, _ = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

        if ids is None:
            return 0

        for i, marker_id in enumerate(ids.flatten()):
            if target_id is None or marker_id == target_id:
                marker_corners=corners[i][0]
                center_x=np.mean(marker_corners[:,0])
                image_center_x=self.resolution[0]/2
                offset=center_x-image_center_x
                print(f"ArUco ID {marker_id} detected, offset:{offset:.1f}px")
                return offset
            
        return 0