import cv2
import robomaster
from robomaster import robot
from robomaster import vision
from InfoType import PointInfo

class LineDetector:
    def __init__(self, ep_robot):
        self.robot = ep_robot
        self.ep_vision = self.robot.vision
        self.lines = []
        self.realLines = []
        self.ep_vision.sub_detect_info(name="line", color="blue", callback=self.on_detect_line)
    def on_detect_line(self, line_info):
        number = len(line_info)
        self.lines.clear()
        line_type = line_info[0]
        # print('line_type', line_type)
        for i in range(1, number):
            x, y, ceta, c = line_info[i]
            self.realLines.append([x,y])
            self.lines.append(PointInfo(x, y, ceta, c))
    def getRealLineInfo(self):
        return self.realLines
    

# class LineFollower:
#     def __init__(self, ep_robot):
#         self.robot = ep_robot
#         self.camera = self.robot.camera
#         self.ep_vision = self.robot.vision
#         self.lineDetector = LineDetector(self.robot)

#     def find_line_center(self, img):
#         # Assuming the blue line is detected in the image
#         # Implement your logic to find the center of the blue line
#         # Return the (x, y) coordinates of the center
#         detectedLines = self.lineDetector.lines
#         for j in range(0, len(detectedLines)):
#             cv2.circle(img, detectedLines[j].pt, 3, detectedLines[j].color, -1)
#         return img

#     def adjust_position(self, line_center_x, img_center_x):
#         # Calculate the deviation
#         deviation = line_center_x - img_center_x

#         # Adjust the robot's position based on the deviation
#         # You might use self.robot.chassis.move() with appropriate x, y, z values
#         pass

#     def follow_line(self):
#         self.camera.start_video_stream(display=True)
#         while True:
#             img = self.camera.read_cv2_image(strategy="newest")
#             processed_img = self.process_image(img)
#             line_center_x = self.find_line_center(processed_img)
#             img_center_x = img.shape[1] / 2

#             self.adjust_position(line_center_x, img_center_x)

#         self.camera.stop_video_stream()

#     def close(self):
#         self.robot.close()




   


