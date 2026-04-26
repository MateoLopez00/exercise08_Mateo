from glob import glob
from setuptools import find_packages, setup

package_name = "uav_local_planner"

setup(
    name=package_name,
    version="0.1.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", [f"resource/{package_name}"]),
        (f"share/{package_name}", ["package.xml"]),
        (f"share/{package_name}/config", glob("config/*.yaml")),
        (f"share/{package_name}/launch", glob("launch/*.launch.py")),
        (f"share/{package_name}/rviz", glob("rviz/*.rviz")),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="Mateo Lopez",
    maintainer_email="mateo@example.com",
    description="Artificial Potential Field local planner for UAV obstacle avoidance.",
    license="GPL-3.0-or-later",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "apf_planner_node = uav_local_planner.apf_planner_node:main",
            "metrics_node = uav_local_planner.metrics_node:main",
        ],
    },
)
