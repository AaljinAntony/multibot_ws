import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import IncludeLaunchDescription


def generate_launch_description():
    # namespace = LaunchConfiguration('namespace')
    ros_gzlaunch = get_package_share_directory('turtlebot_gazebo')
    rvizlaunch = get_package_share_directory('turtlebot_description')
    use_sim_time = LaunchConfiguration('use_sim_time')

    rvizlaunch_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(rvizlaunch, 'launch', 'rviz.launch.py')
        ),
        launch_arguments={'use_sim_time': use_sim_time}.items(),
    )
   

    gzfortress_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(ros_gzlaunch, 'launch', 'gazebo.launch.py')
        ),
        launch_arguments={'use_sim_time': use_sim_time}.items(),
    )

    
 
    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='true',
            description='Use simulation (Gazebo) clock if true'),
        gzfortress_cmd,
        rvizlaunch_cmd
       
    ])