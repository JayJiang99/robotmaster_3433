from robomaster import chassis

class RobotMover:
    def __init__(self, ep_chassis):
        self.ep_chassis = ep_chassis

    def rotate_w_speed(self, z_value, duration=15):
        # Rotate for a specified duration (in seconds)
        # self.ep_chassis.move(z=-30, xy_speed=0.0).wait_for_completed(duration)
        self.ep_chassis.drive_speed(x=0, y=0, z=z_value, timeout=duration)
    
    def move_horizontal_distance(self, y_val, xy_speed = 0.7):
        self.ep_chassis.move(x=0, y=y_val, z=0, xy_speed=xy_speed).wait_for_completed()
    
    def stop(self):
        self.ep_chassis.move(z=0, xy_speed=0).wait_for_completed()
