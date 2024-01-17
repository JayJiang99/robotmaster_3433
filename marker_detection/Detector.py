import cv2
from robomaster import vision
from InfoType import MarkerInfo

# Define the marker detection class
    
class MarkerDetector:
    def __init__(self, ep_vision):
        self.ep_vision = ep_vision
        self.markers = []
        self.ep_vision.sub_detect_info(name="marker", callback=self.on_detect_marker)

    def on_detect_marker(self, marker_info):
        number = len(marker_info)
        self.markers.clear()
        for i in range(number):
            x, y, w, h, info = marker_info[i]
            self.markers.append(MarkerInfo(x, y, w, h, info))
            print("marker:{0} x:{1}, y:{2}, w:{3}, h:{4}".format(info, x, y, w, h))

    def draw_markers(self, img):
        # Update the image with detected markers
        for marker in self.markers:
            
            cv2.rectangle(img, marker.pt1, marker.pt2, (255, 255, 255), 2)
            cv2.putText(img, marker.text, marker.center, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        return img
    

    def close(self):
        self.ep_vision.unsub_detect_info("marker")


# Define the line detection
        
class LineDetector:
    def __init__(self, ep_vision):
        self.ep_vision = ep_vision

    # def close(self):
        