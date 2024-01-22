from robomaster import robot
from robomaster import led
from robomaster import gimbal
import cv2
import time

from Detector import MarkerDetector
from RobotMove import RobotMover


class RobotTask:
    def __init__(self):
        self.ep_robot = robot.Robot()
        self.ep_robot.initialize(conn_type="ap")
        self.ep_vision = self.ep_robot.vision
        self.ep_chassis = self.ep_robot.chassis
        self.ep_camera = self.ep_robot.camera
        # Set travel mode to 'chassis lead'
        self.ep_robot.gimbal.recenter().wait_for_completed()
        self.ep_robot.gimbal.set_follow_chassis(True)
        
        self.detector = MarkerDetector(self.ep_vision)
        self.mover = RobotMover(self.ep_chassis)

    def run_task2_rotate_marker_detection(self):
        print('start')
        self.ep_camera.start_video_stream(display=False)
        self.mover.rotate_w_speed(z_value = 10,duration=15)
        start_time = time.time()
        while time.time() - start_time < 15:
            img = self.ep_camera.read_cv2_image(strategy="newest", timeout=0.5)
            img_with_markers = self.detector.draw_markers(img)
            self.ep_robot.play_sound(filename="hit").wait_for_completed()
            cv2.imshow("Markers", img_with_markers)
            cv2.waitKey(1)
        cv2.destroyAllWindows()
        self.mover.stop()

    def close(self):
        self.ep_robot.close()

if __name__ == '__main__':
    task = RobotTask()
    try:
        task.run_task2_rotate_marker_detection()
    finally:
        task.close()
