# MR-based-drone-controller
This repository contains various methods of drone control.
This package was developed and tested on Ubuntu 18.04 and ROS Melodic.

## Setup:

#### Step 1:
Copy the **drone_control** package from this repository into the src folder of your ROS workspace.

#### Step 2:
Copy the [ROS-TCP-Endpoint](https://github.com/Unity-Technologies/ROS-TCP-Endpoint) into the src folder of your ROS workspace.

#### Step 3:
From [ROS-Unity Integration](https://github.com/Unity-Technologies/Unity-Robotics-Hub/blob/main/tutorials/ros_unity_integration/README.md) copy the **unity_robotics_demo** and **unity_robotics_demo_msgs** packages into the src folder of your ROS workspace.

#### Step 4:
Download the [sjtu-drone](https://github.com/tahsinkose/sjtu-drone) package into the src folder of your ROS workspace.

#### Step 5:

Go to your ROS Workspace through the Terminal and run the following commands:

    catkin_make
    source devel/setup.bash
    
#### Step 6:
Give running permissions to the .py files inside the drone_control package

        chmod +x user_control.py
        chmod +x topic_control.py


## First Controller: Command the sjtu-drone to go to one goal point

This controller will allow you to give one coordinate location tot he drone, and the drone will reach and stay at the goal coordinate autonomously.

#### Launch the sjtu-drone

        roslaunch sjtu_drone simple.launch
        
#### Run the controller
        rosrun drone_control user_control.py 
        
## Second Controller: Control the Drone from Unity

For this type of control, you will have to run Windows in paraller with Ubuntu 18.04 with ROS Melodic installed. You can either use a virtualbox with bridged network connection, or natively run Ubuntu on a separate PC.

On Windows, you will have to install the Unitu HUB with Unity 2020 or above, along with the [MRTK-Toolkit](https://docs.microsoft.com/en-us/windows/mixed-reality/develop/unity/mrtk-getting-started) for interaction.

Also install the [Windows 10 SDK 10.0.18362.0](https://developer.microsoft.com/en-us/windows/downloads/windows-10-sdk/)

The main idea of this type of control is to have a **cube** inside a Unity scene and you can move and drag the cube to control the drone simulation inside Gazebo.

### Setup Unity:

Setup the Unity scene by following the first and third tutorial from [ROS-Unity Integration](https://github.com/Unity-Technologies/Unity-Robotics-Hub/blob/main/tutorials/ros_unity_integration/README.md).

Remove the **plane** object and follow the section **Importing the Mixed Reality Toolkit and Configuring the Unity project** from [this tutorial](https://docs.microsoft.com/en-us/windows/mixed-reality/develop/unity/tutorials/mr-learning-base-02?tabs=openxr) to add the Mixed Reality ToolKit to your project that will enable you to interact with the cube.

### Run the controller

#### On Ubuntu

###### Step 1: ROS-Unity Server Setup
First find the IP address of your Ubuntu by running the following command in your Terminal

        hostname -I
        
Mention this IP in the **params.yaml** file inside the config folder of the ROS-TCP-Endpoint package.

Launch the ROS-Unity Server

        roslaunch ROS-TCP-Endpoint endpoint.launch

This will start the ROS-Unity connection Server.

###### Step 2: Unity Setup
Inside Unity, Open the Robotics/ROS Settings from the Unity menu bar, and set the ROS IP Address variable to the same IP you set inside Ubuntu.

Press the **play** button and you can see the cube rotating. Press **ctrl** and use an optical mouse to click and drag the cube.

###### Step 3: Launch the Drone
Launch the sjtu drone by running the following command

        roslaunch sjtu_drone simple.launch
        
###### Step 4: Launch the Controller
Run the controller node by running the following command
        
        rosrun drone_control topic_control.py 

