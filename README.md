# MR-based-drone-controller
This repository contains various methods of drone control.

## Setup:

#### Step 1:
Copy the 'drone_control' package from this repository into the src folder of your ROS workspace.

#### Step 2:
Copy the [ROS-TCP-Endpoint](https://github.com/Unity-Technologies/ROS-TCP-Endpoint) into the 'src' folder of your ROS workspace.

#### Step 3:
From [ROS-Unity Integration](https://github.com/Unity-Technologies/Unity-Robotics-Hub/blob/main/tutorials/ros_unity_integration/README.md) copy the unity_robotics_demo and unity_robotics_demo_msgs packages into the 'src' folder of your ROS workspace.

#### Step 4:
Download the [sjtu-drone](https://github.com/tahsinkose/sjtu-drone) package into the 'src' folder of your ROS workspace.

#### Step 5:

Go to your ROS Workspace through the Terminal and run the following commands:

    catkin_make
    source devel/setup.bash
    
#### Step 6:
Give running permissions to the .py files inside the drone_control package

        chmod +x user_control.py
        chmod +x topic_control.py


## First Controller: Command the sjtu-drone to go to one goal point

This control will allow you to give one coordinate location tot he drone, and the drone will reach and stay at the goal coordinate autonomously.

#### Launch the sjtu-drone

        roslaunch sjtu_drone simple.launch
        
#### Run the controller
        rosrun drone_control user_control.py 
        


