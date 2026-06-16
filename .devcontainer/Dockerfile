ARG ROS_DISTRO=humble
FROM osrf/ros:$ROS_DISTRO-desktop
ARG USERNAME=aaljin
ARG USER_UID=1000
ARG USER_GID=$USER_UID
# Delete user if it exists in container (e.g Ubuntu Noble: ubuntu)
RUN if id -u $USER_UID ; then userdel `id -un $USER_UID` ; fi

# Create the user
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    #
    # [Optional] Add sudo support. Omit if you don't need to install software after connecting.
    && apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y python3-pip
ENV SHELL=/bin/bash


RUN echo 'export RCUTILS_LOGGING_USE_STDOUT=1' >> /home/aaljin/.bashrc
RUN echo 'export RCUTILS_LOGGING_BUFFERED_STREAM=1' >> /home/aaljin/.bashrc
# Optional, but if you like colored logs:
RUN echo 'export RCUTILS_COLORIZED_OUTPUT=1' >> /home/aaljin/.bashrc
RUN echo 'alias rosdi="sudo apt-get update && rosdep update && rosdep install --from-paths src --ignore-src --rosdistro=$ROS_DISTRO -y"' >> /home/aaljin/.bashrc
RUN echo 'alias cbuild="colcon build"' >> /home/aaljin/.bashrc
RUN echo "source /opt/ros/humble/setup.bash" >> /home/aaljin/.bashrc
RUN echo "source /home/ws/install/setup.bash" >> /home/aaljin/.bashrc
RUN echo 'alias cbs="cd /home/ws && colcon build && source install/setup.bash"' >> /home/aaljin/.bashrc
RUN echo 'alias shumbash="source /opt/ros/humble/setup.bash"' >> /home/aaljin/.bashrc
RUN echo 'alias swbash="source /home/ws/install/setup.bash"' >> /home/aaljin/.bashrc
RUN echo "export IGN_IP=127.0.0.1" >> /home/aaljin/.bashrc

#for cyclone dds
# RUN echo 'export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp' >> /home/aaljin/.bashrc

#for multicontainer docker setup with cyclone dds
# RUN echo 'export CYCLONEDDS_URI="/home/ws/.config/cyclone_DDS/cycloneDDS_config.xml"' >> /home/aaljin/.bashrc

#for dev container with cyclone dds
# RUN echo 'export CYCLONEDDS_URI="/home/ws/.config/cyclone_DDS/cycloneDDS_config_devcontainer.xml"' >> /home/aaljin/.bashrc

# #for zenoh (non dds)
# RUN echo "export RMW_IMPLEMENTATION=rmw_zenoh_cpp" >> /home/aaljin/.bashrc
# RUN echo "export ZENOH_CONFIG_OVERRIDE='listen/endpoints=[\"tcp/0.0.0.0:7447\"]'"  #cmd not complete

RUN echo "export ROS_DOMAIN_ID=42" >> /home/aaljin/.bashrc
RUN echo "ulimit -c 0" >> /home/aaljin/.bashrc





#required packages install, the packages are installed later with rosdep. 
# because rosdep needs to download it everytime, we are cacheing using this file, by downloading and installing now.
# any missing files will be downloaded by rosdep
#packages already installed by base image: GUI and Visualization Tools,Core ROS 2 Middleware, c++ and python libraries, launch file libraries
# Standard Messages,Transforms and Robot Modeling,Build and Development Tools
#gazebo classic install
RUN apt-get update

RUN apt-get install ros-$ROS_DISTRO-gazebo-ros-pkgs -y
#ign gazebo install
RUN apt-get install ros-$ROS_DISTRO-ros-gz -y

#other packages. the ROS_DISTRO env is dclared in the base image
RUN apt-get update && apt-get install -y \
    ros-$ROS_DISTRO-cv-bridge  \
    ros-$ROS_DISTRO-image-geometry \
    ros-$ROS_DISTRO-image-transport \
    libopencv-dev \
    ros-$ROS_DISTRO-message-filters \
    ros-$ROS_DISTRO-laser-geometry \
    ros-$ROS_DISTRO-depth-image-proc \
    ros-$ROS_DISTRO-depthimage-to-laserscan \
    ros-$ROS_DISTRO-robot-localization \
    ros-$ROS_DISTRO-xacro \
    python3-numpy \
    ros-$ROS_DISTRO-nav2-common \
    ros-$ROS_DISTRO-octomap-server \
    ros-$ROS_DISTRO-pointcloud-to-laserscan \
    ros-$ROS_DISTRO-rtabmap-sync \
    ros-$ROS_DISTRO-rtabmap-slam \
    ros-$ROS_DISTRO-rtabmap-viz \
    ros-$ROS_DISTRO-nav2-simple-commander \
    time \
    ros-$ROS_DISTRO-navigation2 \
    ros-$ROS_DISTRO-nav2-bringup \
    wget
    # ros-$ROS_DISTRO-rmw-cyclonedds-cpp \
    # ros-$ROS_DISTRO-rmw-zenoh-cpp
    
RUN apt-get install -y gedit

#for testing the display 
# RUN apt-get install mesa-utils -y



# ********************************************************
# * Anything else you want to do like clean up goes here *
# ********************************************************

RUN apt-get update && apt-get upgrade -y
#cleaning unnececry files
RUN apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

# for docker compose, not for dev container
# COPY --exclude=./build/  --exclude=./install/  --exclude=./log/ --chown=$USERNAME . /home/ws 


# [Optional] Set the default user. Omit if you want to keep the default as root.
USER $USERNAME
CMD ["/bin/bash"]

#for docker compose, not for dev cntainer
# RUN bin/bash -ic "cd /home/ws && sudo apt-get update && rosdep update && rosdep install --from-paths src --ignore-src --rosdistro=$ROS_DISTRO -y && source /home/aaljin/.bashrc && colcon build"