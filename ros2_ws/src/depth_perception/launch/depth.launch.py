from launch import LaunchDescription
from launch_ros.actions import Node
def generate_launch_description():
    return LaunchDescription([
        Node(
            package="depth_perception",
            executable="depth_node",
            name="depth_to_cloud",
            output="screen",
        ),
        Node(
            package="depth_perception",
            executable="ground_segmentation_node",
            name="ground_segmentation",
            output="screen",
        ),
    ])
