# Copyright 2026
# SPDX-License-Identifier: Apache-2.0
"""Pika gripper description-only RViz visualization.

Starts robot_state_publisher, joint_state_publisher(_gui), and RViz2.
"""

from ament_index_python.packages import get_package_share_directory
from launch import LaunchContext, LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
import xacro


def _optional_xacro_args(context: LaunchContext, *names):
    """Forward launch args to xacro only when the user set them."""
    mappings = {}
    for name in names:
        value = context.perform_substitution(LaunchConfiguration(name))
        if value:
            mappings[name] = value
    return mappings


def _spawn_publishers(context: LaunchContext):
    share = get_package_share_directory("pika_gripper_description")
    xacro_path = f"{share}/urdf/pika_gripper_standalone.urdf.xacro"
    joint_states_topic = LaunchConfiguration("joint_states_topic")
    use_joint_state_gui = LaunchConfiguration("use_joint_state_gui")

    mappings = {
        "use_fake_hardware": "true",
        **_optional_xacro_args(context, "xyz", "rpy", "tcp_xyz", "tcp_rpy"),
    }
    robot_description = xacro.process_file(xacro_path, mappings=mappings).toprettyxml(
        indent="  "
    )
    return [
        Node(
            package="robot_state_publisher",
            executable="robot_state_publisher",
            name="robot_state_publisher",
            output="screen",
            parameters=[{"robot_description": robot_description}],
            remappings=[("joint_states", joint_states_topic)],
        ),
        Node(
            package="joint_state_publisher_gui",
            executable="joint_state_publisher_gui",
            name="joint_state_publisher_gui",
            condition=IfCondition(use_joint_state_gui),
            parameters=[{"robot_description": robot_description}],
            remappings=[("joint_states", joint_states_topic)],
        ),
        Node(
            package="joint_state_publisher",
            executable="joint_state_publisher",
            name="joint_state_publisher",
            condition=UnlessCondition(use_joint_state_gui),
            parameters=[{"robot_description": robot_description}],
            remappings=[("joint_states", joint_states_topic)],
        ),
    ]


def generate_launch_description() -> LaunchDescription:
    share = get_package_share_directory("pika_gripper_description")
    use_rviz = LaunchConfiguration("use_rviz")
    rviz_config = PathJoinSubstitution([share, "rviz", "visualize_pika_gripper.rviz"])

    return LaunchDescription(
        [
            DeclareLaunchArgument("xyz", default_value=""),
            DeclareLaunchArgument("rpy", default_value=""),
            DeclareLaunchArgument("tcp_xyz", default_value=""),
            DeclareLaunchArgument("tcp_rpy", default_value=""),
            DeclareLaunchArgument("use_joint_state_gui", default_value="true"),
            DeclareLaunchArgument("use_rviz", default_value="true"),
            DeclareLaunchArgument(
                "joint_states_topic",
                default_value="/pika_gripper_description/joint_states",
            ),
            OpaqueFunction(function=_spawn_publishers),
            Node(
                package="rviz2",
                executable="rviz2",
                name="rviz2",
                arguments=["--display-config", rviz_config],
                condition=IfCondition(use_rviz),
            ),
        ]
    )
