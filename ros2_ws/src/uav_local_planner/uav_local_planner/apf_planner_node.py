import math
from typing import Iterable, List, Optional, Sequence, Tuple

import rclpy
from geometry_msgs.msg import Point, PoseStamped, Twist, Vector3
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import PointCloud2
from sensor_msgs_py import point_cloud2
from std_msgs.msg import Float32
from visualization_msgs.msg import Marker, MarkerArray

Vector = Tuple[float, float, float]


def _norm(vector: Vector) -> float:
    return math.sqrt(vector[0] ** 2 + vector[1] ** 2 + vector[2] ** 2)


def _add(left: Vector, right: Vector) -> Vector:
    return (left[0] + right[0], left[1] + right[1], left[2] + right[2])


def _scale(vector: Vector, factor: float) -> Vector:
    return (vector[0] * factor, vector[1] * factor, vector[2] * factor)


def _clamp_vector(vector: Vector, max_norm: float) -> Vector:
    norm = _norm(vector)
    if norm <= max_norm or norm == 0.0:
        return vector
    return _scale(vector, max_norm / norm)


class ApfPlannerNode(Node):
    """Reactive Artificial Potential Field local planner for a PX4 UAV."""

    def __init__(self) -> None:
        super().__init__("apf_planner_node")

        self.declare_parameters(
            namespace="",
            parameters=[
                ("goal", [8.0, 0.0, 2.5]),
                ("k_att", 0.8),
                ("k_rep", 1.8),
                ("obstacle_influence_radius", 3.0),
                ("safety_radius", 0.9),
                ("max_speed", 1.0),
                ("vertical_speed_limit", 0.5),
                ("goal_tolerance", 0.6),
                ("control_rate", 20.0),
                ("pointcloud_topic", "/camera/depth/points"),
                ("pose_topic", "/mavros/local_position/pose"),
                ("cmd_vel_topic", "/mavros/setpoint_velocity/cmd_vel_unstamped"),
                ("marker_topic", "/uav_local_planner/markers"),
                ("max_points", 800),
                ("min_obstacle_height", -1.0),
                ("max_obstacle_height", 2.0),
                ("command_timeout_sec", 1.0),
                ("world_frame", "map"),
            ],
        )

        self.goal = tuple(float(value) for value in self.get_parameter("goal").value)
        self.k_att = float(self.get_parameter("k_att").value)
        self.k_rep = float(self.get_parameter("k_rep").value)
        self.obstacle_influence_radius = float(
            self.get_parameter("obstacle_influence_radius").value
        )
        self.safety_radius = float(self.get_parameter("safety_radius").value)
        self.max_speed = float(self.get_parameter("max_speed").value)
        self.vertical_speed_limit = float(self.get_parameter("vertical_speed_limit").value)
        self.goal_tolerance = float(self.get_parameter("goal_tolerance").value)
        self.max_points = int(self.get_parameter("max_points").value)
        self.min_obstacle_height = float(self.get_parameter("min_obstacle_height").value)
        self.max_obstacle_height = float(self.get_parameter("max_obstacle_height").value)
        self.command_timeout_sec = float(self.get_parameter("command_timeout_sec").value)
        self.world_frame = str(self.get_parameter("world_frame").value)

        pose_topic = str(self.get_parameter("pose_topic").value)
        pointcloud_topic = str(self.get_parameter("pointcloud_topic").value)
        cmd_vel_topic = str(self.get_parameter("cmd_vel_topic").value)
        marker_topic = str(self.get_parameter("marker_topic").value)
        control_rate = float(self.get_parameter("control_rate").value)

        self.current_position: Optional[Vector] = None
        self.obstacle_points: List[Vector] = []
        self.min_obstacle_distance = math.inf
        self.path_points: List[Point] = []
        self.last_cloud_time = self.get_clock().now()
        self.goal_reached = False

        self.create_subscription(
            PoseStamped,
            pose_topic,
            self._pose_callback,
            qos_profile_sensor_data,
        )
        self.create_subscription(
            PointCloud2,
            pointcloud_topic,
            self._pointcloud_callback,
            qos_profile_sensor_data,
        )
        self.cmd_publisher = self.create_publisher(Twist, cmd_vel_topic, 10)
        self.marker_publisher = self.create_publisher(MarkerArray, marker_topic, 10)
        self.min_distance_publisher = self.create_publisher(
            Float32,
            "/uav_local_planner/min_obstacle_distance",
            10,
        )

        self.create_timer(1.0 / control_rate, self._control_step)
        self.get_logger().info(
            f"APF planner ready: goal={self.goal}, pose={pose_topic}, "
            f"cloud={pointcloud_topic}, cmd={cmd_vel_topic}"
        )

    def _pose_callback(self, msg: PoseStamped) -> None:
        self.current_position = (
            float(msg.pose.position.x),
            float(msg.pose.position.y),
            float(msg.pose.position.z),
        )
        if len(self.path_points) == 0 or self._last_path_point_is_far(self.current_position):
            self.path_points.append(
                Point(
                    x=self.current_position[0],
                    y=self.current_position[1],
                    z=self.current_position[2],
                )
            )
            self.path_points = self.path_points[-500:]

    def _pointcloud_callback(self, msg: PointCloud2) -> None:
        self.obstacle_points = self._extract_points(msg)
        self.min_obstacle_distance = min(
            (_norm(point) for point in self.obstacle_points),
            default=math.inf,
        )
        self.last_cloud_time = self.get_clock().now()

    def _extract_points(self, msg: PointCloud2) -> List[Vector]:
        points: List[Vector] = []
        cloud: Iterable[Sequence[float]] = point_cloud2.read_points(
            msg,
            field_names=("x", "y", "z"),
            skip_nans=True,
        )

        for point in cloud:
            if len(points) >= self.max_points:
                break
            x = float(point[0])
            y = float(point[1])
            z = float(point[2])
            distance = math.sqrt(x * x + y * y + z * z)

            if distance <= 0.05 or distance > self.obstacle_influence_radius:
                continue
            if z < self.min_obstacle_height or z > self.max_obstacle_height:
                continue
            points.append((x, y, z))

        return points

    def _control_step(self) -> None:
        if self.current_position is None:
            self._publish_stop()
            return

        distance_to_goal = _norm(
            (
                self.goal[0] - self.current_position[0],
                self.goal[1] - self.current_position[1],
                self.goal[2] - self.current_position[2],
            )
        )
        if distance_to_goal <= self.goal_tolerance:
            if not self.goal_reached:
                self.get_logger().info("Goal reached. Publishing zero velocity.")
            self.goal_reached = True
            self._publish_stop()
            self._publish_markers((0.0, 0.0, 0.0), distance_to_goal)
            return

        self.goal_reached = False
        force = _add(self._attractive_force(), self._repulsive_force())
        velocity = _clamp_vector(force, self.max_speed)
        velocity = (
            velocity[0],
            velocity[1],
            max(-self.vertical_speed_limit, min(self.vertical_speed_limit, velocity[2])),
        )

        self._publish_velocity(velocity)
        self._publish_min_distance()
        self._publish_markers(velocity, distance_to_goal)

    def _attractive_force(self) -> Vector:
        assert self.current_position is not None
        return (
            self.k_att * (self.goal[0] - self.current_position[0]),
            self.k_att * (self.goal[1] - self.current_position[1]),
            self.k_att * (self.goal[2] - self.current_position[2]),
        )

    def _repulsive_force(self) -> Vector:
        force = (0.0, 0.0, 0.0)
        for obstacle in self.obstacle_points:
            distance = _norm(obstacle)
            if distance <= 0.05 or distance > self.obstacle_influence_radius:
                continue

            effective_distance = max(distance - self.safety_radius, 0.05)
            magnitude = self.k_rep * (
                (1.0 / effective_distance) - (1.0 / self.obstacle_influence_radius)
            ) / (effective_distance * effective_distance)

            away = (-obstacle[0] / distance, -obstacle[1] / distance, -obstacle[2] / distance)
            force = _add(force, _scale(away, magnitude))

        return _clamp_vector(force, self.max_speed * 2.0)

    def _publish_velocity(self, velocity: Vector) -> None:
        msg = Twist()
        msg.linear.x = velocity[0]
        msg.linear.y = velocity[1]
        msg.linear.z = velocity[2]
        self.cmd_publisher.publish(msg)

    def _publish_stop(self) -> None:
        self.cmd_publisher.publish(Twist())

    def _publish_min_distance(self) -> None:
        msg = Float32()
        msg.data = (
            float(self.min_obstacle_distance)
            if math.isfinite(self.min_obstacle_distance)
            else -1.0
        )
        self.min_distance_publisher.publish(msg)

    def _publish_markers(self, velocity: Vector, distance_to_goal: float) -> None:
        markers = MarkerArray()
        markers.markers.append(self._goal_marker())
        markers.markers.append(self._velocity_marker(velocity))
        markers.markers.append(self._path_marker())
        markers.markers.append(self._obstacle_marker())
        self.marker_publisher.publish(markers)

        if int(self.get_clock().now().nanoseconds / 1e9) % 5 == 0:
            self.get_logger().debug(
                f"distance_to_goal={distance_to_goal:.2f}, "
                f"min_obstacle_distance={self.min_obstacle_distance:.2f}"
            )

    def _goal_marker(self) -> Marker:
        marker = self._base_marker(0, "goal", Marker.SPHERE)
        marker.pose.position.x = self.goal[0]
        marker.pose.position.y = self.goal[1]
        marker.pose.position.z = self.goal[2]
        marker.scale = Vector3(x=0.4, y=0.4, z=0.4)
        marker.color.r = 0.1
        marker.color.g = 0.9
        marker.color.b = 0.1
        marker.color.a = 1.0
        return marker

    def _velocity_marker(self, velocity: Vector) -> Marker:
        marker = self._base_marker(1, "apf_velocity", Marker.ARROW)
        marker.scale = Vector3(x=0.08, y=0.16, z=0.16)
        marker.color.r = 0.1
        marker.color.g = 0.4
        marker.color.b = 1.0
        marker.color.a = 1.0

        if self.current_position is None:
            return marker

        start = Point(
            x=self.current_position[0],
            y=self.current_position[1],
            z=self.current_position[2],
        )
        end = Point(
            x=self.current_position[0] + velocity[0],
            y=self.current_position[1] + velocity[1],
            z=self.current_position[2] + velocity[2],
        )
        marker.points = [start, end]
        return marker

    def _path_marker(self) -> Marker:
        marker = self._base_marker(2, "path", Marker.LINE_STRIP)
        marker.scale.x = 0.05
        marker.color.r = 1.0
        marker.color.g = 0.8
        marker.color.b = 0.0
        marker.color.a = 1.0
        marker.points = self.path_points
        return marker

    def _obstacle_marker(self) -> Marker:
        marker = self._base_marker(3, "local_obstacles", Marker.POINTS)
        marker.scale.x = 0.08
        marker.scale.y = 0.08
        marker.color.r = 1.0
        marker.color.g = 0.1
        marker.color.b = 0.1
        marker.color.a = 0.7

        if self.current_position is None:
            return marker

        marker.points = [
            Point(
                x=self.current_position[0] + point[0],
                y=self.current_position[1] + point[1],
                z=self.current_position[2] + point[2],
            )
            for point in self.obstacle_points[:200]
        ]
        return marker

    def _base_marker(self, marker_id: int, namespace: str, marker_type: int) -> Marker:
        marker = Marker()
        marker.header.frame_id = self.world_frame
        marker.header.stamp = self.get_clock().now().to_msg()
        marker.ns = namespace
        marker.id = marker_id
        marker.type = marker_type
        marker.action = Marker.ADD
        marker.pose.orientation.w = 1.0
        return marker

    def _last_path_point_is_far(self, position: Vector) -> bool:
        last = self.path_points[-1]
        distance = math.sqrt(
            (last.x - position[0]) ** 2
            + (last.y - position[1]) ** 2
            + (last.z - position[2]) ** 2
        )
        return distance > 0.2


def main(args: Optional[List[str]] = None) -> None:
    rclpy.init(args=args)
    node = ApfPlannerNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
