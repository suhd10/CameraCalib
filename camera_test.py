import cv2
import numpy as np

from utils import deproject_pixel_to_point,transform_img2angle
from detection_thread import DetectionThread

# 実装時は消そうね
angle = None

np.seterr(all="ignore")
aruco = cv2.aruco

mtx = np.load('mtx.npy')
dist = np.load('dist.npy')

x_center = round(mtx[0][2])
y_center = round(mtx[1][2])

detection_thread = DetectionThread()
detection_thread.start()
# VideoCapture オブジェクトを取得
capture = cv2.VideoCapture(0,cv2.CAP_DSHOW)
#capture = cv2.VideoCapture(0)

# フレームサイズ等の設定
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
capture.set(cv2.CAP_PROP_FPS, 60)

try:
    while(True):
        ret, frame = capture.read()
        if not ret:
            continue

        frame_array = np.asanyarray(frame) # ndarrayに変換
        
        if not detection_thread.event.is_set():
            detection_thread.color_frame = cv2.resize(frame_array, (1280, 720))
            detection_thread.event.set()

        # 画像表示
        color_image_s = cv2.resize(frame_array, (1280, 720))

        if detection_thread.result is None:
            print("None")
            continue
        #print(detection_thread.result.mean_xy)
        if (detection_thread.result.mean_xy[0] != -1) and (detection_thread.result.mean_xy[1] != -1): # マーカが検出された場合
            result = detection_thread.result
            aruco.drawDetectedMarkers(color_image_s, result.corners, result.ids, (0,255,0)) #検出したマーカ情報を元に，原画像に描画する
            angle = transform_img2angle(mtx, dist, result.mean_xy[0], result.mean_xy[1])
            
            cv2.drawMarker(color_image_s, (round(result.mean_xy[0]), round(result.mean_xy[1])), (0, 255, 0),
                           markerType=cv2.MARKER_CROSS, markerSize=20, thickness=2, line_type=cv2.LINE_AA)
        else:  # 検出されなかった時
            cv2.putText(color_image_s,
                        "marker: Not detected",
                        (25, 25),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        (0, 255, 0),
                        2,
                        cv2.LINE_4)
        
        # 角度誤差表示
        if angle is not None:
            cv2.putText(color_image_s,
                    f"Angle Error x: {round(angle[0],2)} deg",
                    (25, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 0),
                    2,
                    cv2.LINE_4)
            cv2.putText(color_image_s,
                    f"Angle Error y: {round(angle[1],2)} deg",
                    (25, 75),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 0),
                    2,
                    cv2.LINE_4)
        
        # 中心線描画
        cv2.line(color_image_s, pt1=(0, y_center),pt2=(1280, y_center), color=(0,255,0), thickness=2, lineType=cv2.LINE_AA, shift=0)
        cv2.line(color_image_s, pt1=(x_center,0),pt2=(x_center, 720), color=(0,255,0), thickness=2, lineType=cv2.LINE_AA, shift=0)

        cv2.namedWindow('Camera', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('Camera', color_image_s)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    capture.release()
    cv2.destroyAllWindows()
    detection_thread.finish()