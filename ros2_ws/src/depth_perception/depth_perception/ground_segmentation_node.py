import numpy as np
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2
from sensor_msgs_py import point_cloud2 as pc2

from depth_perception.depth_node import make_pointcloud2


def fit_plane(points):
    p1, p2, p3 = points
    normal = np.cross(p2 - p1, p3 - p1)
    norm = np.linalg.norm(normal)
    if norm < 1e-6:
        return None
    normal = normal / norm
    d = -np.dot(normal, p1)
    return np.array([normal[0], normal[1], normal[2], d], dtype=np.float32)


def plane_distances(plane, points):
    return np.abs(points @ plane[:3] + plane[3])


class GroundSegmentation(Node):
    def __init__(self):
        super().__init__("ground_segmentation")
        self.sub = self.create_subscription(PointCloud2, "/perception/points", self.cb, 5)
        self.pub_g = self.create_publisher(PointCloud2, "/perception/points_ground", 5)
        self.pub_o = self.create_publisher(PointCloud2, "/perception/points_obstacles", 5)
    def cb(self, msg: PointCloud2):
        pts = np.array(
            [
                [point[0], point[1], point[2]]
                for point in pc2.read_points(msg, field_names=("x", "y", "z"), skip_nans=True)
            ],
            dtype=np.float32,
        )
        if pts.shape[0] < 100:
            return

        candidate_mask = np.isfinite(pts).all(axis=1) & (pts[:, 2] > 0.1) & (pts[:, 2] < 30.0)
        candidates = pts[candidate_mask]
        if candidates.shape[0] < 100:
            return

        rng = np.random.default_rng(42)
        best_inliers = None
        best_plane = None

        for _ in range(200):
            sample_idx = rng.choice(candidates.shape[0], size=3, replace=False)
            plane = fit_plane(candidates[sample_idx])
            if plane is None:
                continue

            distances = plane_distances(plane, candidates)
            inliers = distances < 0.08

            if best_inliers is None or inliers.sum() > best_inliers.sum():
                best_inliers = inliers
                best_plane = plane

        if best_inliers is None or best_inliers.sum() < 50:
            self.get_logger().warn("Could not estimate a stable ground plane.")
            return

        ground = candidates[best_inliers]
        obstacles = candidates[~best_inliers]
        self.pub_g.publish(make_pointcloud2(msg.header, ground))
        self.pub_o.publish(make_pointcloud2(msg.header, obstacles))


def main(args=None):
    rclpy.init(args=args)
    node = GroundSegmentation()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
