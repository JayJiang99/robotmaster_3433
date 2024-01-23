from robomaster import robot
from robomaster import led
from robomaster import gimbal
from robomaster import blaster

import cv2
import time

from Detector import MarkerDetector
from RobotMove import RobotMover
from LineFollower import LineDetector

class RobotTask:
    def __init__(self):
        print('initialization')
        self.ep_robot = robot.Robot()
        self.ep_robot.initialize(conn_type="ap")
        self.ep_vision = self.ep_robot.vision
        self.ep_chassis = self.ep_robot.chassis
        self.ep_camera = self.ep_robot.camera
        # Set travel mode to 'chassis lead'
        # self.ep_robot.set_robot_mode(mode=robot.GIMBAL_LEAD)
        # self.ep_robot.gimbal.recenter().wait_for_completed()
        self.ep_robot.gimbal.set_follow_chassis(True)
    
        self.detector = MarkerDetector(self.ep_robot)
        self.mover = RobotMover(self.ep_chassis)
        self.lineDetector = LineDetector(self.ep_robot)
    def run_task1(self):
        print('start')
        self.ep_robot.gimbal.moveto(pitch=0, yaw=0).wait_for_completed()
        self.ep_camera.start_video_stream(display=False)
        start_time = time.time()
        while time.time() - start_time < 5:
            img = self.ep_camera.read_cv2_image(strategy="newest", timeout=0.5)
            img_with_markers = self.detector.draw_markers(img)
            cv2.imshow("Markers", img_with_markers)
            cv2.waitKey(1)
        cv2.destroyAllWindows()
        self.mover.stop()

    def run_task2_rotate_marker_detection(self):
        print('start')
        self.ep_camera.start_video_stream(display=False)
        self.mover.rotate_w_speed(z_value = 10,duration=5)
        start_time = time.time()
        while time.time() - start_time < 15:
            img = self.ep_camera.read_cv2_image(strategy="newest", timeout=0.5)
            img_with_markers = self.detector.draw_markers(img)
            
            cv2.imshow("Markers", img_with_markers)
            cv2.waitKey(1)
        cv2.destroyAllWindows()
        self.mover.stop()
    def run_task3(self):
        print('start')
        self.ep_camera.start_video_stream(display=False)
        start_time = time.time()
        while time.time() - start_time < 5:
            img = self.ep_camera.read_cv2_image(strategy="newest", timeout=0.5)
            lines = self.lineDetector.getRealLineInfo()
            print(lines[0])
            cv2.circle(img, [round(lines[0][0]*1280), round(lines[0][1]*720)], 5,0)
            self.mover.move_xydistance(lines[0][0] - 0.5,lines[0][1] - 0.5)
            cv2.imshow("Lines", img)
            cv2.waitKey(1)
        cv2.destroyAllWindows()
        self.mover.stop()
    def close(self):
        self.ep_robot.close()

if __name__ == '__main__':
    task = RobotTask()
    try:
        task.run_task1()
    finally:
        task.close()
