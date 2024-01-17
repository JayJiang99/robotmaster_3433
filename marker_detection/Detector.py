import cv2
from robomaster import vision

class MarkerInfo:

    def __init__(self, x, y, w, h, info):
        self._x = x
        self._y = y
        self._w = w
        self._h = h
        self._info = info

    @property
    def pt1(self):
        return int((self._x - self._w / 2) * 1280), int((self._y - self._h / 2) * 720)

    @property
    def pt2(self):
        return int((self._x + self._w / 2) * 1280), int((self._y + self._h / 2) * 720)

    @property
    def center(self):
        return int(self._x * 1280), int(self._y * 720)

    @property
    def text(self):
        return self._info
    
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

    def detect_markers(self, img):
        # Update the image with detected markers
        for marker in self.markers:
            cv2.rectangle(img, marker.pt1, marker.pt2, (255, 255, 255), 2)
            cv2.putText(img, marker.text, marker.center, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        return img
    
    def draw_markers(self,img):

        return img

    def close(self):
        self.ep_vision.unsub_detect_info("marker")