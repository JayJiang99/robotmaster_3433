from robomaster import robot
import time
from Detector import MarkerDetector
from RobotMove import RobotMover
import cv2

class RobotTask:
    def __init__(self):
        self.ep_robot = robot.Robot()
        self.ep_robot.initialize(conn_type="ap")
        self.ep_vision = self.ep_robot.vision
        self.ep_chassis = self.ep_robot.chassis
        self.ep_camera = self.ep_robot.camera
        
        self.detector = MarkerDetector(self.ep_vision)
        self.mover = RobotMover(self.ep_chassis)

    def run_task_rotate_marker_detection(self):
        self.ep_camera.start_video_stream(display=False)
        self.mover.rotate_w_speed(z_value = 10,duration=15)
        start_time = time.time()
        while time.time() - start_time < 15:
            img = self.ep_camera.read_cv2_image(strategy="newest", timeout=0.5)
            img_with_markers = self.detector.draw_markers(img)
            cv2.imshow("Markers", img_with_markers)
            cv2.waitKey(1)
        cv2.destroyAllWindows()
        self.mover.stop()

    def close(self):
        self.ep_robot.close()

if __name__ == '__main__':
    task = RobotTask()
    try:
        task.run_task_rotate_marker_detection()
    finally:
        task.close()
