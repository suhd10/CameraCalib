import pyrealsense2 as rs
from intrinsics_pickleable import IntrinsicsPickleable

config = rs.config()
config.enable_stream(rs.stream.color, 640, 360, rs.format.bgr8, 30)
config.enable_stream(rs.stream.depth, 640, 360, rs.format.z16, 30)

# ストリーミング開始
pipeline = rs.pipeline()
profile = pipeline.start(config)
# Alignオブジェクト生成
align_to = rs.stream.color
align = rs.align(align_to)

color_intr = rs.video_stream_profile(
    profile.get_stream(rs.stream.color)
).get_intrinsics()
print(color_intr)
# intr_pickleable = IntrinsicsPickleable(
#     color_intr.coeffs,
#     color_intr.fx,
#     color_intr.fy,
#     color_intr.height,
#     color_intr.model,
#     color_intr.ppx,
#     color_intr.ppy,
#     color_intr.width
# )
xyz = rs.rs2_deproject_pixel_to_point(color_intr, [100, 100], 1)
print(xyz)