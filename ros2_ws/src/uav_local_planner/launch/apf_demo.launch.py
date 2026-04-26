import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    package_share = get_package_share_directory("uav_local_planner")
    params_file = os.path.join(package_share, "config", "apf_params.yaml")
    rviz_file = os.path.join(package_share, "rviz", "apf_demo.rviz")

    use_rviz = LaunchConfiguration("use_rviz")
    output_csv = LaunchConfiguration("output_csv")

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "use_rviz",
                default_value="true",
                description="Start RViz2 with the APF visualization config.",
            ),
            DeclareLaunchArgument(
                "output_csv",
                default_value="/root/docs/results_static.csv",
                description="CSV path for metrics output inside the container.",
            ),
            Node(
                package="uav_local_planner",
                executable="apf_planner_node",
                name="apf_planner_node",
                output="screen",
                parameters=[params_file],
            ),
            Node(
                package="uav_local_planner",
                executable="metrics_node",
                name="metrics_node",
                output="screen",
                parameters=[params_file, {"output_csv": output_csv}],
            ),
            Node(
                package="rviz2",
                executable="rviz2",
                name="rviz2",
                arguments=["-d", rviz_file],
                condition=IfCondition(use_rviz),
                output="screen",
            ),
        ]
    )
