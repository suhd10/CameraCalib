import math
import numpy as np


def deproject_pixel_to_point(intrinsics, dist, pixcel_x: int, pixcel_y: int, depth: int) -> list:
    """
    カメラの内部パラメータと歪みパラメータを用いて、カメラ座標系における3次元点を計算する
    intrinsics: camera matrix
    pixcel_x: x coordinate of the pixel
    pixcel_y: y coordinate of the pixel
    return: 3D point in camera coordinate
    """

    x = (pixcel_x - intrinsics[0][2]) / intrinsics[0][0]
    y = (pixcel_y - intrinsics[1][2]) / intrinsics[1][1]
    
    r2 = x*x + y*y
    f = 1 + dist[0] * r2 + dist[1] * r2*r2 + dist[4] * r2*r2*r2
    ux = x*f + 2*dist[2]*x*y + dist[3]*(r2 + 2*x*x)
    uy = y*f + 2*dist[3]*x*y + dist[2]*(r2 + 2*y*y)
    point = [depth * ux, depth * uy, depth]
    return point

def transform_img2angle(intrinsics, dist, pixcel_x: int, pixcel_y:int) -> list:
    """
    カメラ画像の座標からロボット座標の水平角に変換する
    :param pixel_x: カメラ画像横のピクセル(左→右)
    :param pixel_y: カメラ画像縦のピクセル(上→下)
    :param intrinsics: カメラの内部パラメータ(realsense)
    :return: ロボットから見た水平角(deg)
    """
    xyz = deproject_pixel_to_point(intrinsics, dist, pixcel_x, pixcel_y, 1)
    angle = [-math.atan2(xyz[0], xyz[2]) * 180 / math.pi, -math.atan2(xyz[1], xyz[2]) * 180 / math.pi]

    return angle