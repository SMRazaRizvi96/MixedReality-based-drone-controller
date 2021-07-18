# MR-based-drone-controller

The main idea of this project is to developed a Mixed-Reality based Reliable controller for Drones.

## Hardware
    Hololens2
    DJI Tello Drone
    Laptop
    
## Usage
The drone pilot will be wearing a Hololens2 in which a Cube hologram will augment the vision of the Drone. The drone pilot can see the hologram, and also the drone in the line of sight.
In order to control the drone, the pilot only have to pick the cube hologram, and place it to where the pilot wants the drone to go, and the drone will reach the coordinate of the hologram autonomously.

## Software Architecture
The Robot Operating System (ROS1) is used to design the software architecture to provide a communication between the Hololens2 and the DJI Tello drone.
On the other hand, in order to develop the Mixed Reality scene for the Hololens2, a UNity project is created and a Universal Windows Platform application is built to be deployed on the Hololens through Visual Studio.

### Specific Software Versions
    Ubuntu 18.04 running in Virtual Box
    ROS Melodic
    Unity Hub 2.4.3
    Unity 2020.3.13f1
    Visual Studio 2019


#### Note:
This repository is still in the development phase. You will find various ROS nodes created for the Drone simulation, and others for the actual DJI Tello drone.

#### Developer:
[Syed Muhammad Raza Rizvi](https://github.com/SMRazaRizvi96)

## Setup:

#### Step 1:
Copy the **drone_control** package from this repository into the src folder of your ROS workspace.

#### Step 2:
Clone the [ROS-TCP-Endpoint](https://github.com/Unity-Technologies/ROS-TCP-Endpoint) into the src folder of your ROS workspace.

#### Step 3:
From [ROS-Unity Integration](https://github.com/Unity-Technologies/Unity-Robotics-Hub/blob/main/tutorials/ros_unity_integration/README.md) clone the **unity_robotics_demo** and **unity_robotics_demo_msgs** packages into the src folder of your ROS workspace.

#### Step 4:
Clone the [sjtu-drone](https://github.com/tahsinkose/sjtu-drone) package into the src folder of your ROS workspace.

#### Step 5:

Go to your ROS Workspace through the Terminal and run the following commands:

    catkin_make
    source devel/setup.bash
    
#### Step 6:
Give running permissions to the .py files inside the drone_control package

        chmod +x user_control.py
        chmod +x topic_control.py


## First Controller | Simulation: Command the simulated sjtu-drone to go to one goal point

This controller will allow you to give one coordinate location to the drone, and the drone will reach and stay at the goal coordinate autonomously.

#### Launch the sjtu-drone

        roslaunch sjtu_drone simple.launch
        
#### Run the controller

        rosrun drone_control user_control.py
        
   Now give the x, y, z coordinates as the goal coordinate for the drone.
        
        
        
## Second Controller | Simulation: Control the Simulated Drone from Unity

This controller will allow you to run a Unity scene inside Unity in which you can see and move a Hologram Cube. The coordinates of this hologram will be sent through TCP from Unity to ROS, and will be used as goal coordinates for the simulated drone.

For this type of control, you will have to run Windows in paraller with Ubuntu 18.04 with ROS Melodic installed. You can either use a virtualbox with bridged network connection, or natively run Ubuntu on a separate PC.

On Windows, you will have to install the Unitu HUB with Unity 2020 or above, along with the [MRTK-Toolkit](https://docs.microsoft.com/en-us/windows/mixed-reality/develop/unity/mrtk-getting-started) for interaction.

Also install the [Windows 10 SDK 10.0.18362.0](https://developer.microsoft.com/en-us/windows/downloads/windows-10-sdk/)

The main idea of this type of control is to have a **cube** inside a Unity scene and you can move and drag the cube to control the drone simulation inside Gazebo.

### Step 1: Setup Unity:

Setup the Unity scene by following the first and third tutorial from [ROS-Unity Integration](https://github.com/Unity-Technologies/Unity-Robotics-Hub/blob/main/tutorials/ros_unity_integration/README.md).

Remove the **plane** object and follow the section **Importing the Mixed Reality Toolkit and Configuring the Unity project** from [this tutorial](https://docs.microsoft.com/en-us/windows/mixed-reality/develop/unity/tutorials/mr-learning-base-02?tabs=openxr) to add the Mixed Reality ToolKit to your project that will enable you to interact with the cube.

### Step 2: Launch the sjtu-drone

        roslaunch sjtu_drone simple.launch


### Step 3: ROS-Unity Server Setup on Ubuntu
First find the IP address of your Ubuntu by running the following command in your Terminal

        hostname -I
        
Mention this IP in the **params.yaml** file inside the config folder of the ROS-TCP-Endpoint package.

Launch the ROS-Unity Server

        roslaunch ros_tcp_endpoint endpoint.launch

This will start the ROS-Unity connection Server.

        
### Step 4: Launch the Controller in Ubuntu
Run the controller node by running the following command
        
        rosrun drone_control topic_control.py 

### Step 5: Run the Unity Project
Inside Unity, Open the Robotics/ROS Settings from the Unity menu bar, and set the ROS IP Address variable to the same IP you set inside Ubuntu.

Press the **play** button and you can see the cube rotating. Press **ctrl** and use an optical mouse to click and drag the cube.

You can now move the cube in Unity, and can see the Simulated Drone moving inside ROS Gazebo.


## Third Controller | DJI Tello drone: Control the DJI Tello Drone by sending commands from ROS

This controller allows you to send UDP packets containing control commands to the DJI Tello drone.
See the [Tello SDK](https://dl-cdn.ryzerobotics.com/downloads/Tello/Tello%20SDK%202.0%20User%20Guide.pdf) for a list of acceptable commands.

### Step 1: Launch the sjtu-drone

    roslaunch sjtu_drone simple.launch

### Step 2: Run the Controller:

    rosrun drone_control tello_server.py 
    
First send 'command' to enable the drone to now start receiving SDK Commands.
The send the control commands to the DJI Tello.

## Fourth Controller | DJI Tello drone: Control the DJI Tello Drone from Unity OR the Hololens2

This controller allows you to send UDP packets containing control commands to the DJI Tello drone.
See the [Tello SDK](https://dl-cdn.ryzerobotics.com/downloads/Tello/Tello%20SDK%202.0%20User%20Guide.pdf) for a list of acceptable commands.

At first the controller will allow you to send commands to the Drone.
Later on, if now you want the drone to track the Hologram, you can type 'track', and as done by the second controller, the DJI Tello drone will now use the coordinates of the Cube as the goal coordinates and will reach there autonomously.

### Step 1: ROS-Unity Server Setup on Ubuntu
First find the IP address of your Ubuntu by running the following command in your Terminal

        hostname -I
        
Mention this IP in the **params.yaml** file inside the config folder of the ROS-TCP-Endpoint package.

Launch the ROS-Unity Server

        roslaunch ros_tcp_endpoint endpoint.launch

This will start the ROS-Unity connection Server.

### Step 2: Run the Unity Project
Inside Unity, Open the Robotics/ROS Settings from the Unity menu bar, and set the ROS IP Address variable to the same IP you set inside Ubuntu.

Press the **play** button and you can see the cube rotating. Press **ctrl** and use an optical mouse to click and drag the cube.

You can now move the cube in Unity, and can see the Simulated Drone moving inside ROS Gazebo.

OR

Build the 'Universal Windows Platform' application from Unity, and then deploy this application on the Hololens2 to interact with the cube.

### Step 3: Run the Controller

    rosrun drone_control tello_server_subtopic.py 
    
Now you can just type the command to send and can see the DJI Tello executing these commands.

## Fifth Controller | DJI Tello drone: Control the DJI Tello Drone using the tellopy library

This controller is a very basic ROS node exploiting the tellopy library to send control commands to the DJI Tello drone.

### Run the Controller

    rosrun drone_control tello_server_library.py 



