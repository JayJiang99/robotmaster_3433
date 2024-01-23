import cv2
from robomaster import vision
from robomaster import robot

from InfoType import MarkerInfo

# Define the marker detection class
    
class MarkerDetector:
    def __init__(self, ep_robot):
        self.robot = ep_robot
        self.ep_vision = self.robot.vision
        self.markers = []
        self.ep_vision.sub_detect_info(name="marker", callback=self.on_detect_marker_2)
    
    
    def on_detect_marker(self, marker_info):
        number = len(marker_info)
        # Save marker info
        self.markers.clear()
        for i in range(number):
            x, y, w, h, info = marker_info[i]
            self.markers.append(MarkerInfo(x, y, w, h, info))
            self.robot.play_sound(robot.SOUND_ID_SHOOT).wait_for_completed()
            print("marker:{0} x:{1}, y:{2}, w:{3}, h:{4}".format(info, x, y, w, h))
            
    def on_detect_marker_2(self, marker_info):
        
        number = len(marker_info)
            
        # Save marker info
        self.markers.clear()
        for i in range(number):
            x, y, w, h, info = marker_info[i]
            self.markers.append(MarkerInfo(x, y, w, h, info))
            print("marker:{0} x:{1}, y:{2}, w:{3}, h:{4}".format(info, x, y, w, h))
            self.align_gimbal_to_marker(x, y)
    def align_gimbal_to_marker(self, x_marker, y_marker):
        x_sight = 0.5
        y_sight = 0.5
        # Calculate the angle to rotate gimbal
        yaw_rotation = 96 * (x_marker - x_sight)
        pitch_rotation = 54 * (y_marker - y_sight)
        print('align2')
        print(yaw_rotation)
        print(pitch_rotation)
        # Rotate gimbal to align with marker
        self.robot.gimbal.move(pitch=pitch_rotation, yaw=yaw_rotation).wait_for_completed()

        # Turn on trajectory light and shoot 5 times
        self.robot.blaster.set_led(brightness=255, effect=self.robot.blaster.LED_ON)
        self.robot.blaster.fire(times=5)
        self.robot.blaster.set_led(brightness=0, effect=self.robot.blaster.LED_OFF)

    def draw_markers(self, img):
        # Update the image with detected markers
        for marker in self.markers:
            
            cv2.rectangle(img, marker.pt1, marker.pt2, (255, 255, 255), 2)
            cv2.putText(img, marker.text, marker.center, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        return img
    

    def close(self):
        self.ep_vision.unsub_detect_info("marker")

# class GimbalMarkerTrack:
#     def __init__(self, ep_robot):
#         self.robot = ep_robot
#         self.ep_vision = self.robot.vision
#         self.ep_gimbal = self.robot.gimbal
#         self.markers = []
#         self.ep_vision.sub_detect_info(name="marker", callback=self.on_detect_marker)
#         self.ep_gimbal.sub_angle(freq = 5, callback=self.sub_data_handler)
#     def on_detect_marker(self, marker_info):
#         number = len(marker_info)  
#         # Save marker info
#         self.markers.clear()
#         for i in range(number):
#             x, y, w, h, info = marker_info[i]
#             self.markers.append(MarkerInfo(x, y, w, h, info))
#             print("marker:{0} x:{1}, y:{2}, w:{3}, h:{4}".format(info, x, y, w, h))
#             self.align_gimbal_to_marker(x, y)
#     def align_gimbal_to_marker(self, x_marker, y_marker):
#         # Get the current gimbal position
        
#         x_sight = 0.5
#         y_sight = 0.5
#         print('align')
#         # Calculate the angle to rotate gimbal
#         yaw_rotation = 96 * (x_marker - x_sight)
#         pitch_rotation = 54 * (y_marker - y_sight)
#         print('align2')
#         # Rotate gimbal to align with marker
#         self.robot.gimbal.moveto(pitch=pitch_rotation, yaw=yaw_rotation).wait_for_completed()

#         # Turn on trajectory light and shoot 5 times
#         self.robot.blaster.set_led(brightness=255, effect=self.robot.blaster.LED_ON)
#         self.robot.blaster.fire(times=5)
#         self.robot.blaster.set_led(brightness=0, effect=self.robot.blaster.LED_OFF)
    
#     def sub_data_handler(self, angle_info):
#         self.pitch_angle, self.yaw_angle, self.pitch_ground_angle, self.yaw_ground_angle = angle_info
#         # print("gimbal angle: pitch_angle:{0}, yaw_angle:{1}, pitch_ground_angle:{2}, yaw_ground_angle:{3}".format(
#         # pitch_angle, yaw_angle, pitch_ground_angle, yaw_ground_angle))

#     def draw_markers(self, img):
#         # Update the image with detected markers
#         for marker in self.markers:
            
#             cv2.rectangle(img, marker.pt1, marker.pt2, (255, 255, 255), 2)
#             cv2.putText(img, marker.text, marker.center, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
#         return img
    

#     def close(self):
#         self.ep_vision.unsub_detect_info("marker")

# Define the line detection
        
class LineDetector:
    def __init__(self, ep_vision):
        self.ep_vision = ep_vision

    # def close(self):
        