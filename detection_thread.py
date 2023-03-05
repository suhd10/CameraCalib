from threading import Event, Thread
import numpy as np
import cv2
import time

class DetectedData:
    def __init__(self, mean_xy, corners, ids):
        self.mean_xy = mean_xy
        self.corners = corners
        self.ids = ids

class DetectionThread:
    def __init__(self):
        self.finished = False
        self.event = Event()
        self.running = False
        self.thread = Thread(target=self.run)

        self.aruco = cv2.aruco
        self.dictionary =  self.aruco.getPredefinedDictionary(self.aruco.DICT_4X4_50)   # ARマーカーは「4x4ドット，ID番号50まで」の辞書を使う
        self.color_frame = None
        self.result = None
        self.r_time = None

    def start(self):
        self.thread.start()

    def finish(self):
        self.finished = True
        self.event.set()

    def run(self):
        while not self.finished:
            self.event.wait()
            self.detection()
            self.event.clear()

    def detection(self):
        if self.color_frame is None:
            print("color_frame is None")
            return
        dictionary = self.dictionary
        color_frame = self.color_frame
        corners, ids, rejectedImgPoints = self.aruco.detectMarkers(color_frame, dictionary) #マーカを検出
        if len(corners) > 0:
            mean_xy = np.mean(corners[0][0],axis=0)
        else:
            mean_xy = [-1, -1]
        result = DetectedData(mean_xy, corners, ids)
        self.r_time = time.time()
        self.result = result