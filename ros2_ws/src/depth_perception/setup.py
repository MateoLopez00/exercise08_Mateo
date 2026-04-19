from setuptools import find_packages, setup

package_name = "depth_perception"

setup(
    name=package_name,
    version="0.0.1",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
        ("share/" + package_name + "/launch", ["launch/depth.launch.py"]),
        ("share/" + package_name + "/rviz", ["rviz/depth.rviz"]),
    ],
    install_requires=["setuptools", "numpy"],
    zip_safe=True,
    maintainer="Mateo Lopez",
    maintainer_email="you@example.com",
    description="Depth + point cloud + ground segmentation",
    license="Apache-2.0",
    entry_points={
        "console_scripts": [
            "depth_node = depth_perception.depth_node:main",
            "ground_segmentation_node = depth_perception.ground_segmentation_node:main",
        ],
    },
)
