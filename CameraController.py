import time
import threading
from DJITelloPy.api import Tello
import cv2


class CameraController:

    def __init__(self, tello):
        self.lock = threading.Lock()
        self.tello = tello

    # some kind of mutex lock needs to go here to switch safely between the front and bottom cameras

    def get_bottom_cam(self, tello):
        self.lock.acquire()

        tello.streamon()
        tello.set_video_direction(Tello.CAMERA_DOWNWARD)
        tello.set_video_fps(Tello.FPS_30)
        try:
            while True:
                img = tello.get_frame_read().frame
                cv2.imshow('bottom_cam', img)
                cv2.waitKey(1)
        except KeyboardInterrupt:
            exit(1)
        finally:
            self.lock.release()

    def get_front_cam(self, tello):
        self.lock.acquire()

        tello.streamon()
        tello.set_video_direction(Tello.CAMERA_FORWARD)
        tello.set_video_fps(Tello.FPS_30)
        # resolution and bitrate
        try:
            while True:
                img = tello.get_frame_read().frame
                cv2.imshow('front_cam', img)
                cv2.waitKey(1)
        except KeyboardInterrupt:
            exit(1)
        finally:
            self.lock.release()

    def run_front_cam(self):
        front_camera = threading.Thread(target=self.get_front_cam, args=(self.tello,), daemon=True, name='front-camera')
        front_camera.start()

    def run_bottom_cam(self):
        bottom_camera = threading.Thread(target=self.get_bottom_cam, args=(self.tello,), daemon=True, name='bottom-camera')
        bottom_camera.start()

    def kill_cam(self):
        self.tello.streamoff()
        self.tello.streamon()


#
# tello = Tello()
# tello.connect()
# print(tello.get_battery())
# c = CameraController()
# # c.run_front()
# # c.run_bottom()
#
# time.sleep(30)
#
# exit(1)






