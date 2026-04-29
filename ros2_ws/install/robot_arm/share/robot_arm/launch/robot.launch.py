import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    pkg_dir = get_package_share_directory('robot_arm')
    urdf_path = os.path.join(pkg_dir, 'urdf', 'robot_arm.urdf')
    rviz_config_path = os.path.join(pkg_dir, 'rviz', 'robot.rviz')

    with open(urdf_path, 'r') as f:
        robot_description = f.read()

    return LaunchDescription([

        # Publishes robot_description parameter + TF from URDF fixed joints
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{'robot_description': robot_description}],
        ),

        Node(
            package='robot_arm',
            executable='tf_publisher', 
        ),

        Node(
            package='robot_arm',
            executable='pose_publisher', 
            output='screen'
        ),

        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen',
            arguments=['-d', rviz_config_path],
        )

    ])
