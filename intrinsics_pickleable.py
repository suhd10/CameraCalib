from dataclasses import dataclass
from typing import Any

import pyrealsense2 as rs

@dataclass
class IntrinsicsPickleable:
    coeffs: Any
    fx: float
    fy: float
    height: int
    model: Any
    ppx: float
    ppy: float
    width: int

    def to_intrinsics(self):
        obj = rs.intrinsics()
        obj.coeffs = self.coeffs
        obj.fx = self.fx
        obj.fy = self.fy
        obj.height = self.height
        obj.model = self.model
        obj.ppx = self.ppx
        obj.ppy = self.ppy
        obj.width = self.width
        return obj