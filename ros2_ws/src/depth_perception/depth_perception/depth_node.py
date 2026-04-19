import cv2
import numpy as np
import rclpy
from cv_bridge import CvBridge
from message_filters import ApproximateTimeSynchronizer, Subscriber
from rclpy.node import Node
from sensor_msgs.msg import CameraInfo, Image, PointCloud2, PointField
from std_msgs.msg import Header


def make_pointcloud2(header, points_xyz, colors_rgb=None):
    n = points_xyz.shape[0]
    if colors_rgb is None:
        fields = [
            PointField(name="x", offset=0, datatype=PointField.FLOAT32, count=1),
            PointField(name="y", offset=4, datatype=PointField.FLOAT32, count=1),
            PointField(name="z", offset=8, datatype=PointField.FLOAT32, count=1),
        ]
        data = points_xyz.astype(np.float32).tobytes()
        point_step = 12
    else:
        fields = [
            PointField(name="x", offset=0, datatype=PointField.FLOAT32, count=1),
            PointField(name="y", offset=4, datatype=PointField.FLOAT32, count=1),
            PointField(name="z", offset=8, datatype=PointField.FLOAT32, count=1),
            PointField(name="rgb", offset=12, datatype=PointField.FLOAT32, count=1),
        ]
        rgb = colors_rgb.astype(np.uint32)
        packed_rgb = (rgb[:, 0] << 16) | (rgb[:, 1] << 8) | rgb[:, 2]
        packed_rgb = packed_rgb.view(np.float32)
        arr = np.zeros(
            n,
            dtype=[("x", "f4"), ("y", "f4"), ("z", "f4"), ("rgb", "f4")],
        )
        arr["x"] = points_xyz[:, 0]
        arr["y"] = points_xyz[:, 1]
        arr["z"] = points_xyz[:, 2]
        arr["rgb"] = packed_rgb
        data = arr.tobytes()
        point_step = 16
    msg = PointCloud2()
    msg.header = header
    msg.height = 1
    msg.width = n
    msg.fields = fields
    msg.is_bigendian = False
    msg.point_step = point_step
    msg.row_step = point_step * n
    msg.is_dense = True
    msg.data = data
    return msg


class DepthToCloud(Node):
    def __init__(self):
        super().__init__("depth_to_cloud")
        self.bridge = CvBridge()
        self.fx = None
        self.fy = None
        self.cx = None
        self.cy = None
        self.create_subscription(
            CameraInfo,
            "/camera/color/camera_info",
            self.info_cb,
            10,
        )
        rgb_sub = Subscriber(self, Image, "/camera/color/image")
        depth_sub = Subscriber(self, Image, "/camera/depth/image")
        self.sync = ApproximateTimeSynchronizer(
            [rgb_sub, depth_sub],
            queue_size=10,
            slop=0.1,
        )
        self.sync.registerCallback(self.frame_cb)
        self.pub_cloud = self.create_publisher(PointCloud2, "/perception/points", 5)

    def info_cb(self, msg: CameraInfo):
        self.fx = msg.k[0]
        self.fy = msg.k[4]
        self.cx = msg.k[2]
        self.cy = msg.k[5]

    def frame_cb(self, rgb_msg: Image, depth_msg: Image):
        if self.fx is None:
            return
        rgb = self.bridge.imgmsg_to_cv2(rgb_msg, "bgr8")
        depth = self.bridge.imgmsg_to_cv2(depth_msg)

        if depth.dtype == np.uint16:
            depth = depth.astype(np.float32) * 0.001

        if depth.ndim == 3:
            depth = depth[:, :, 0]

        h, w = depth.shape

        if rgb.shape[:2] != (h, w):
            rgb = cv2.resize(rgb, (w, h), interpolation=cv2.INTER_LINEAR)

        rgb = cv2.cvtColor(rgb, cv2.COLOR_BGR2RGB)

        u = np.tile(np.arange(w), h)
        v = np.repeat(np.arange(h), w)
        z = depth.flatten()

        valid = (z > 0.1) & (z < 30.0) & np.isfinite(z)
        u = u[valid]
        v = v[valid]
        z = z[valid]

        x = (u - self.cx) * z / self.fx
        y = (v - self.cy) * z / self.fy

        points = np.stack([x, y, z], axis=1)
        colors = rgb.reshape(-1, 3)[valid]

        header = Header()
        header.stamp = depth_msg.header.stamp
        header.frame_id = "camera_link"

        self.pub_cloud.publish(make_pointcloud2(header, points, colors))


def main(args=None):
    rclpy.init(args=args)
    node = DepthToCloud()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
