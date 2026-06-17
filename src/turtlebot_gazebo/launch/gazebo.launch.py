import os
import xacro
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, TimerAction
from launch.substitutions import Command
from launch.substitutions import LaunchConfiguration
from launch.substitutions import PythonExpression
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import IncludeLaunchDescription
from launch.actions import AppendEnvironmentVariable
from launch.actions import GroupAction
from launch_ros.actions import PushRosNamespace
from nav2_common.launch import RewrittenYaml

def generate_launch_description():
    
    ld=[]
    
    
    
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    # robot_no = LaunchConfiguration('no_of_robots')
    # namespace = LaunchConfiguration('namespace')
    ros_gz_sim = get_package_share_directory('ros_gz_sim')
    # tortoisebot_slam= get_package_share_directory('tortoisebot_slam')
    world= os.path.join(get_package_share_directory('turtlebot_gazebo'), 'worlds','hospital.sdf')
    gazebo_package= get_package_share_directory('turtlebot_gazebo')
    set_env_vars_resources = AppendEnvironmentVariable(
            'GZ_SIM_RESOURCE_PATH',
            os.path.join(gazebo_package,'models'))
    known_init_poses = LaunchConfiguration("known_init_poses")
    
    ekf_config=os.path.join(gazebo_package,'params','ekf.yaml')
    # laserfilter
    laser_filter_params=os.path.join(gazebo_package,"params", "laser_filter.yaml")
    
    slam_params_file = LaunchConfiguration('slam_params_file')
    declare_slam_params_file_cmd = DeclareLaunchArgument(
        'slam_params_file',
        default_value=os.path.join(get_package_share_directory("tortoisebot_slam"),
                                   'config', 'mapper_params_online_async_map.yaml'),
        description='Full path to the ROS2 parameters file to use for the slam_toolbox node')
    
    # m_explore_package=get_package_share_directory('m-explore-ros2')
    explore_config=os.path.join(gazebo_package,'params','explore.yaml')
    nav_package= get_package_share_directory('tortoisebot_navigation')
    nav_params=os.path.join(nav_package,'params','nav2_params.yaml')
    merge_config = os.path.join(gazebo_package, "params", "merge_map.yaml"
    )
    # slam_toolbox=get_package_share_directory('slam_toolbox')
    frontier_node_params_file=os.path.join(gazebo_package,'params','frontier_explore.yaml')
    
    declare_known_init_poses_argument = DeclareLaunchArgument(
        "known_init_poses",
        default_value="false",
        description="Known initial poses of the robots. If so don't forget to declare them in the params.yaml file",
    )

    
    
    
    # set_env_vars_resources2 = AppendEnvironmentVariable(
    #         'GZ_SIM_RESOURCE_PATH',
    #         os.path.join(get_package_share_directory('turtlebot_gazebo'),
    #                     'photos'))
    ####for testing-------->
    # declare_namespace =DeclareLaunchArgument(
    #     'namespace',
    #     default_value= 'jndsjcjdbjdb'
    #     )
    ####<-----
    
    #number of robots to be spawned
    num_robot=2

    ##intitial spawning points
    init_x=5
    init_y=5
    init_z=0.1
    #distance between the next spawn robot
    dist_x=0
    dist_y=-2
    dist_z=0
    
    
    # robot_name= ['robot1','robot2']
    # robots = {
    #     'robot1':{
    #         'x':str(x),
    #         'y':str(y),
    #         'z':str(z)
    #     },
    #     'robot2':{
    #         'x':str(x),
    #         'y':str(y-2),
    #         'z':str(z)
    #     },
    #     'robot3':{
    #         'x':str(x),
    #         'y':str(y-5),
    #         'z':str(z)
    #     }
    # }
    x=init_x
    y=init_y
    z=init_z
    robots={}#empty dictionary
    #adding robot names and pose to the dictionary
    for i in range(num_robot):
        robots.update({
            f'robot{i+1}':{
                'x':str(x),
                'y':str(y),
                'z':str(z)
            }
        })
        x=x+dist_x
        y=y+dist_y
        z=z+dist_z
    #if needed to overwite the dictionary
    # robots.update({
    #         'robotn':{  #replace n with robot number
    #             'x':'0',  #replace x,y,z cordinates
    #             'y':'1',
    #             'z':'0.1'
    #         }
    #     })
    
    
    
    urdf = os.path.join(
        get_package_share_directory('turtlebot_description'),
        'urdf',
        'turtlebot3_waffle_pi.urdf.xacro')
    gzserver_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(ros_gz_sim, 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={'gz_args': ['-r -s -v4 ', world], 'on_exit_shutdown': 'true'}.items()
    )
    gzclient_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(ros_gz_sim, 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={'gz_args': '-g -v4 '}.items()
    )
    bridge_params = os.path.join(
        get_package_share_directory('turtlebot_gazebo'),
        'params',
        'bridge.yaml'
    )
    start_gazebo_ros_bridge_cmd_tf = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        name='tf_and_clock_only_bridge',
        arguments=[
            # '/tf@tf2_msgs/msg/TFMessage[ignition.msgs.Pose_V',
            '/clock@rosgraph_msgs/msg/Clock[ignition.msgs.Clock'
        ],
        output='screen',
    )
    
    #list for return functions 
    ld.append(set_env_vars_resources)
    ld.append(gzserver_cmd)
    ld.append(gzclient_cmd)
    ld.append(start_gazebo_ros_bridge_cmd_tf)
    ld.append(declare_slam_params_file_cmd)
    ld.append(declare_known_init_poses_argument)
    
    # remap_for_map_merge_node_2=[]
  
    print(robots)
    loop=0 
    for robot_n in robots:
        loop=loop+1
        print("loop",loop)  #testing
        # robot_desc= xacro.process(urdf)
        namespace=''
        namespace=robot_n
        print('namespace = ',namespace) 
        robot_desc = Command([
            'xacro ',
            urdf,
            ' namespace:=',
            f'{namespace}/'            
        ])
        # remappings = []
        # remappings = [("/tf", f"/{namespace}/tf"), ("/tf_static", f"/{namespace}/tf_static")]
        remappings = [("/tf", "tf"), ("/tf_static", "tf_static")]




        robot_description_node=Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            output='screen',
            namespace=namespace,
            # name=f'{robot_n}robot_state_publisher',
            parameters=[
                {
                    'robot_description': robot_desc,
                    'use_sim_time': use_sim_time,
                    'frame_prefix': ''
                }
            ],
            remappings=remappings 
        )
        start_gazebo_ros_spawner_cmd = Node(
            package='ros_gz_sim',
            executable='create',
            name=f'{robot_n}_spawner',
            arguments=[
                '-name', f'{namespace}/turtlebot',
                '-topic',f'{namespace}/robot_description',
                '-x', f'{robots[robot_n]["x"]}',
                '-y', f'{robots[robot_n]["y"]}',
                '-z', f'{robots[robot_n]["z"]}'
            ],
            output='screen',
            remappings=remappings 

        )
        # node_tf2_static_scan = Node(
        #     name='tf2_ros_scan_fix',
        #     package='tf2_ros',
        #     executable='static_transform_publisher',
        #     output='screen',
        #     namespace=namespace,
        #     arguments=['-0.064', '0', '0.122', '0.0', '0.0', '0.0', f'{namespace}/base_footprint', f'{namespace}/base_scan'] 
        # )
        
                


        start_gazebo_ros_bridge_cmd = Node(
            package='ros_gz_bridge',
            executable='parameter_bridge',
            namespace=namespace,
            name='bridge',
            parameters=[
                {'config_file':bridge_params},
                {'expand_gz_topic_names':True}
                ],
            arguments=[],
            output='screen'
        )
        # imu_helper_node = ExecuteProcess(
        #     cmd=['python3', os.path.join(
        #         get_package_share_directory('turtlebot_gazebo'),
        #         'launch',
        #         'imu_covariance_helper.py'
        #     ), '--ros-args', '-r', f'__ns:=/{namespace}', '-p', 'use_sim_time:=true'],
        #     output='screen'
        # )
        robot_localization_node = Node(
            package='robot_localization',
            executable='ekf_node',
            name='ekf_filter_node',
            output='screen',
            namespace=namespace,
            parameters=[ekf_config,
                        {
                        'odom_frame':f'{namespace}/odom',
                        'base_link_frame':f'{namespace}/base_footprint',
                        'world_frame':f'{namespace}/odom',
                        'odom0':f'/{namespace}/odom',
                        'imu0':f'/{namespace}/imu',#/imu/corrected' if convariance helper
                        'use_sim_time':use_sim_time }],
            remappings=remappings 
        )
        laser_filter=Node(
            package="laser_filters",
            executable="scan_to_scan_filter_chain",
            namespace=namespace,
            parameters=[laser_filter_params,
                        {
                            'use_sim_time': use_sim_time,
                            'filter1.params.box_frame':f'{namespace}/base_footprint'
                        }
                ],
            remappings=remappings + [('scan',f'/{namespace}/scan'),
                        ('scan_filtered',f'/{namespace}/lidar_scan')]
        )
        start_async_slam_toolbox_node = Node(
            parameters=[
            slam_params_file,
            {
                'use_sim_time': use_sim_time,
                'odom_frame':f'{namespace}/odom',
                'base_frame':f'{namespace}/base_footprint',
                'scan_topic':f'/{namespace}/lidar_scan',
                'map_frame':f'{namespace}/map'
                }
            ],
            namespace=namespace,
            package='slam_toolbox',
            executable='async_slam_toolbox_node',
            name='slam_toolbox',
            output='screen',
            remappings=remappings+[('/map','map')], 
        )
        
        # multi_slam_cmd = IncludeLaunchDescription(
        #     PythonLaunchDescriptionSource(
        #         os.path.join(slam_toolbox, 'launch', 'online_async_decentralized_multirobot_launch.py')
        #     ),
        #     launch_arguments={'namespace':namespace,
        #                       'use_sim_time':use_sim_time,
        #                       'slam_params_file':slam_params_file}.items()
        # )
        
        
        
        
        
        # #opening the nav parameters yaml
        # with open(nav_params,'r') as f:
        #     nav_params_original=f.read()
        # # replacing the data with ROBOT_NAMESPACE to the vaiable namespace
        # nav_params_temp=nav_params_original.replace('ROBOT_NAMESPACE',namespace)
        # #creating new empty file with namespace in the name
        # temp_nav_params_location=f'/tmp/{namespace}_nav_params.yaml'
        # # writing the replaced params to the new file
        # with open(temp_nav_params_location,'w') as f:
        #     f.write(nav_params_temp)
        
        navigation_node=GroupAction([
            PushRosNamespace(namespace),        
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    os.path.join(nav_package, 'launch', 'navigation_launch.py')
                ),
                launch_arguments={
                    'namespace':namespace,
                    'params_file':nav_params, #new temporay file
                    'use_sim_time':use_sim_time
                    }.items()
            )
        ])

        # m_explore_node = Node(
        #     package="explore_lite",
        #     name="explore_node",
        #     namespace=namespace,
        #     executable="explore",
        #     parameters=[explore_config, 
        #                 {
        #                     "use_sim_time": use_sim_time,
        #                     'robot_base_frame':f'{namespace}/base_footprint',
        #                     'costmap_topic':f'/{namespace}/map',
        #                     'costmap_updates_topic':f'/{namespace}/map_updates'                            
        #                 }
        #                 ],
        #     output="screen",
        #     remappings=remappings,
        # )
        
        
        
        # using these substitues for the robot1 to handle long range and robot2 to handle the corner and other details.
        if namespace=='robot1':
            frontier_node_substitute={
                'weight_distance_wd':'0.4',
                'weight_gain_ws':'2.5',
                'max_linear_speed_vmax':'1.0',
                'max_angular_speed_wmax':'1.0',
                'sensor_effective_range_m':'3.0'
            }
        elif namespace=='robot2':
            frontier_node_substitute={
                'weight_distance_wd':'2.5',
                'weight_gain_ws':'0.4',
                'max_linear_speed_vmax':'0.50',
                'max_angular_speed_wmax':'1.0',
                'sensor_effective_range_m':'1.0'
            } 
        else:
            frontier_node_substitute={}
            print('frontier node substitue empty. need to configure for more robots')
            
        frontier_node = Node(
            package="frontier_exploration_ros2",
            executable="frontier_explorer",
            name="frontier_explorer",
            namespace=namespace,
            output="screen",
            arguments=["--ros-args", "--log-level", 'info'],
            parameters=[
                frontier_node_params_file,
                {
                    'robot_base_frame':f'{namespace}/base_footprint',
                    'global_frame':f'{namespace}/map'
                },
                frontier_node_substitute
            ],
            remappings=remappings
        )
        
        
        map_merge_substitutions = {
            'use_sim_time': use_sim_time,
            'known_init_poses': known_init_poses,
            'world_frame': f"{namespace}/map" # Sets /robot1/map or /robot2/map
        }

        # Run the memory-safe rewriter tool
        configured_merge_params = RewrittenYaml(
            source_file=merge_config,
            root_key=namespace,          # Automatically nests parameters under /robotX/map_merge
            param_rewrites=map_merge_substitutions,
            convert_types=True           # Casts string "false" into a native boolean false
        )
        map_merge_node = Node(
            package="multirobot_map_merge",
            name="map_merge",
            namespace=namespace,
            executable="map_merge",
            parameters=[
                configured_merge_params,           
            ],
            output="screen",
            remappings=remappings,
        )   
        
     
        # rmapping to add to the merge node 2
        # remap_for_map_merge_node_2.append((f'/map{loop}',f'/{namespace}/map'))
        # print('remap merge=',remap_for_map_merge_node_2)
        
        delayed_slam = TimerAction(
            period=10.0,             # Delay duration in seconds (e.g., 10.0 seconds)
            actions=[start_async_slam_toolbox_node] # The launch action(s) to execute after the timer expires
        )
        
        delayed_nav = TimerAction(
            period=20.0,             # Delay duration in seconds (e.g., 10.0 seconds)
            actions=[navigation_node] # The launch action(s) to execute after the timer expires
        )
        delayed_exp = TimerAction(
            period=40.0,             # Delay duration in seconds (e.g., 10.0 seconds)
            actions=[frontier_node] # The launch action(s) to execute after the timer expires
        )
        delayed_map_merge_node = TimerAction(
            period=22.0,             # Delay duration in seconds (e.g., 10.0 seconds)
            actions=[map_merge_node] # The launch action(s) to execute after the timer expires
        )
    
        
            
        #appending the fuctions to run in the list (ld)
        ld.append(robot_description_node)
        ld.append(start_gazebo_ros_spawner_cmd)
        # ld.append(node_tf2_static_scan)
        ld.append(start_gazebo_ros_bridge_cmd)
        # ld.append(imu_helper_node)
        ld.append(robot_localization_node)
        ld.append(laser_filter)
        ld.append(delayed_slam)
        ld.append(delayed_nav)
        ld.append(delayed_exp)
        ld.append(delayed_map_merge_node)  

    

            # Launch merge_map with robot_count argument
    # print('merge node reached')
    # merge_map_launch = ExecuteProcess(
    #     cmd=['ros2', 'launch', 'merge_map', 'merge_map_launch.py', ['robot_count:=',num_robot]],
    #     output='screen'
    # )
    # merge_map_launch = IncludeLaunchDescription(
    #     PythonLaunchDescriptionSource(
    #         os.path.join(get_package_share_directory("merge_map"), 'launch', 'merge_map_launch.py')
    #     ),
    #     launch_arguments={'robot_count:=',num_robot}.items()
    # )
    # merge_map_launch=Node(
    #         package='merge_map',
    #         executable='merge_map',
    #         name='merge_map',
    #         output='screen',
    #         parameters=[{'frame_id': 'merge_map'},
    #                      {'robot_count':num_robot},
    #                      {'use_sim_time': True}]
    #     )
    # print('merge node started')
    # ld.append(merge_map_launch)
    # print('control_node reached')
    # Launch multi_robot_exploration control with robot_count argument
    # control_node = ExecuteProcess(
    #     cmd=['ros2', 'run', 'multi_robot_exploration', 'control', '--ros-args', '-p', ['robot_count:=',num_robot]],
    #     output='screen'
    # )
    # control_node = Node(
    #         package="multi_robot_exploration",
    #         name="multi_explore",
    #         # namespace=namespace,
    #         executable="control",
    #         parameters=[
    #             {'robot_count':num_robot}          
    #         ],
    #         output="screen",
    #         # remappings=remappings,
    #     )  
    # print('control node started')
    # ld.append(control_node)
    # map_merge_node_2=Node(
    #     package='merge_map',
    #     executable='merge_map',
    #     output='screen',
    #     name='map_merge_node_2',
    #     parameters=[{'use_sim_time': True}],
    #     remappings=remap_for_map_merge_node_2,
    # )
  


    
    return LaunchDescription(ld)