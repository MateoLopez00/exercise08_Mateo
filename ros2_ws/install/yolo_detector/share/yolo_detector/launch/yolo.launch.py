from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument("model", default_value="yolov8n.pt"),
        DeclareLaunchArgument("conf", default_value="0.25"),
        DeclareLaunchArgument("image_topic", default_value="/camera/color/image"),
        Node(
            package="yolo_detector",
            executable="detector_node",
            name="yolo_detector",
            output="screen",
            parameters=[{
                "model": LaunchConfiguration("model"),
                "conf": LaunchConfiguration("conf"),
                "image_topic": LaunchConfiguration("image_topic"),
            }],
        ),
    ])
