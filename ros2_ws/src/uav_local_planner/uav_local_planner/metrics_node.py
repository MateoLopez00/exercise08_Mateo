import csv
import math
import os
from typing import List, Optional, Tuple

import rclpy
from geometry_msgs.msg import PoseStamped
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from std_msgs.msg import Float32

Vector = Tuple[float, float, float]


def _distance(left: Vector, right: Vector) -> float:
    return math.sqrt(
        (left[0] - right[0]) ** 2
        + (left[1] - right[1]) ** 2
        + (left[2] - right[2]) ** 2
    )


class MetricsNode(Node):
    """Writes simple CSV metrics for the local planner demo."""

    def __init__(self) -> None:
        super().__init__("metrics_node")
        self.declare_parameters(
            namespace="",
            parameters=[
                ("goal", [8.0, 0.0, 2.5]),
                ("goal_tolerance", 0.6),
                ("pose_topic", "/mavros/local_position/pose"),
                ("obstacle_distance_topic", "/uav_local_planner/min_obstacle_distance"),
                ("output_csv", "/root/docs/results_static.csv"),
            ],
        )

        self.goal = tuple(float(value) for value in self.get_parameter("goal").value)
        self.goal_tolerance = float(self.get_parameter("goal_tolerance").value)
        self.output_csv = str(self.get_parameter("output_csv").value)
        pose_topic = str(self.get_parameter("pose_topic").value)
        obstacle_distance_topic = str(self.get_parameter("obstacle_distance_topic").value)

        self.start_time = self.get_clock().now()
        self.last_position: Optional[Vector] = None
        self.path_length = 0.0
        self.min_obstacle_distance = math.inf
        self.success = False
        self.rows_written = 0

        self.create_subscription(
            PoseStamped,
            pose_topic,
            self._pose_callback,
            qos_profile_sensor_data,
        )
        self.create_subscription(
            Float32,
            obstacle_distance_topic,
            self._obstacle_distance_callback,
            10,
        )
        self.create_timer(1.0, self._write_row)
        self._prepare_csv()
        self.get_logger().info(f"Writing planner metrics to {self.output_csv}")

    def _prepare_csv(self) -> None:
        directory = os.path.dirname(self.output_csv)
        if directory:
            os.makedirs(directory, exist_ok=True)
        with open(self.output_csv, "w", newline="", encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(
                [
                    "elapsed_sec",
                    "x",
                    "y",
                    "z",
                    "distance_to_goal",
                    "path_length",
                    "path_efficiency",
                    "min_obstacle_distance",
                    "success",
                ]
            )

    def _pose_callback(self, msg: PoseStamped) -> None:
        position = (
            float(msg.pose.position.x),
            float(msg.pose.position.y),
            float(msg.pose.position.z),
        )
        if self.last_position is not None:
            step = _distance(self.last_position, position)
            if step < 5.0:
                self.path_length += step
        self.last_position = position

        if _distance(position, self.goal) <= self.goal_tolerance:
            self.success = True

    def _obstacle_distance_callback(self, msg: Float32) -> None:
        if msg.data >= 0.0:
            self.min_obstacle_distance = min(self.min_obstacle_distance, float(msg.data))

    def _write_row(self) -> None:
        if self.last_position is None:
            return

        elapsed = (self.get_clock().now() - self.start_time).nanoseconds / 1e9
        distance_to_goal = _distance(self.last_position, self.goal)
        straight_line = max(_distance((0.0, 0.0, 0.0), self.goal), 0.001)
        efficiency = straight_line / max(self.path_length, straight_line)
        min_distance = (
            self.min_obstacle_distance if math.isfinite(self.min_obstacle_distance) else -1.0
        )

        with open(self.output_csv, "a", newline="", encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(
                [
                    f"{elapsed:.2f}",
                    f"{self.last_position[0]:.3f}",
                    f"{self.last_position[1]:.3f}",
                    f"{self.last_position[2]:.3f}",
                    f"{distance_to_goal:.3f}",
                    f"{self.path_length:.3f}",
                    f"{efficiency:.3f}",
                    f"{min_distance:.3f}",
                    int(self.success),
                ]
            )
        self.rows_written += 1

        if self.rows_written % 10 == 0:
            self.get_logger().info(
                f"metrics: success={self.success}, path_length={self.path_length:.2f}, "
                f"min_obstacle_distance={min_distance:.2f}"
            )


def main(args: Optional[List[str]] = None) -> None:
    rclpy.init(args=args)
    node = MetricsNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
