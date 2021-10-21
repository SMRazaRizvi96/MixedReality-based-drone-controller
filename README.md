# MR-based-drone-controller

This project contains a Mixed-Reality based controller for UAV Pilots.

## Hardware
    Hololens2
    DJI Tello Drone
    Laptop
    
## Usage
The drone pilot will be wearing a Hololens2 that will augment the pilot's vision with a drone hologram and some useful information related to the drone control. The drone pilot will drag and drop the drone hologram to control the drone in the line of sight, and the drone will reach the coordinate of the hologram autonomously.

## Software Specifications
    Ubuntu 20.04 running inside a Virtual Box
    ROS Melodic installed in Ubuntu 20.04
    Unity Hub 2.4.3
    Unity 2020.3.13f1
    Visual Studio 2019

## Software Architecture
The Robot Operating System (ROS1) is used to design the software architecture to provide a communication between the Hololens2 and Ubuntu, and from Ubuntu to the DJI Tello drone.
On the other hand, in order to develop the Mixed Reality scene for the Hololens2, a Unity project is created, and a Universal Windows Platform application is built to be deployed on the Hololens through Visual Studio.

#### Developer:
[Syed Muhammad Raza Rizvi](https://github.com/SMRazaRizvi96)
smrazarizvi96@gmail.com

## Setup:


#### Setting up the Drone Controller inside ROS

• Download and Install the Virtual Box in Windows

• Download the Ubuntu 20.04 ISO file, and install it’s Virtual Machine on the Virtual Box

• Bridge the Wireless and Ethernet adapters inside the Virtual Machine form the network settings of the Virtual Machine

• Turn on the Tello drone and face it towards the ArUco markers wall

• Connect the WiFi to Tello’s WiFi, and Ethernet with a local network

• Install ROS Melodic inside Ubuntu 20.04

• Create a ROS Workspace

• Clone the [ROS-TCP-Endpoint](https://github.com/Unity-Technologies/ROS-TCP-Endpoint) into the src folder of your ROS workspace.  
This will allow a communication between Unity and ROS.

• From [ROS-Unity Integration](https://github.com/Unity-Technologies/Unity-Robotics-Hub/blob/main/tutorials/ros_unity_integration/README.md) clone the **unity_robotics_demo** and **unity_robotics_demo_msgs** packages into the src folder of your ROS workspace insude Ubuntu.

• Clone the [Tello Drover](https://github.com/appie-17/tello_driver) ROS package inside the src folder of your ROS Workspace

• Clone the [ArUco ROS](https://github.com/pal-robotics/aruco_ros) package inside the src folder of your ROS Workspace

• Clone the project’s repository inside the src folder of your ROS Workspace, and delete the MR-Controller-Hololens folder

• Build the ROS Workspace using the ’catkin_make’ command

• Give running permissions to all the .py files inside the drone_control package

• Find the hostname of the Ubuntu by typing *’hostname -I’* inside the terminal

• The above command will give two IP addresses because of the two network connections.
Note down the IP Address of the Ubuntu assigned by the local network that will NOT start with 192.xxx.xx.x

• Mention this IP Address inside the config -> params file of the ROS TCP Endpoint package

• Launch the endpoint.launch file of the ROS TCP Endpoint package to launch the ROS TCP Server on the mentioned IP Address

• In order to launch the Joypad controller node, launch the joy_node.launch launch file of the drone_control package of this project

• In order to launch the Mixed-Reality based drone controller, launch the MR-Drone-Controller.launch launch file of the drone_control package of this project


#### Setting up the Mixed Reality Application - Hololens 2

• Download and Install the Unity Hub on Windows

• Download and Install Unity version 2020.3.12f1

• Clone the GitHub repository inside Windows

• Open the Unity project from the MR-Controller-Hololens folder

• Write the ROS IP Address inside the Robotics tab of the Unity project. This IP Address is same as the one mentioned in the ROS TCP Endpoint params file

• Build the UWP application from Unity and open the solution in Visual Studio

• Set the Solution Configuration parameter to ’Release’, and the Solution Platforms to ’ARM6’

• Turn on the Hololens 2 and connect it to the local internet connection through the local network’s WiFi

• Find the IP Address assigned to the Hololens, and mention it inside the Machine Name parameter of the debugging properties, inside the visual studio solution

• Ask the drone pilot to wear the Hololens and stand at the starting calibration position

• Now upload the Unity project on to the Hololens by running the Visual Studio application

## Usage:

#### Using the Mixed Reality Controller

• Measure the calibration constants such as the transformation constants x, y, z, between the ArUco markers from the ArUco marker with Identity 1, and the distance of the
ArUco marker identity 1 from the Hololens reference frame.

• Mention these constants inside the AruCo Tello pose ROS Node

• Launch the Mixed-Reality based drone controller using the *MR-Drone-Controller.launch* launch file of the drone_control package of this project

• This will launch all the required nodes from all the packages

• Type ’takeoff’ to allow the drone to take off

• As soon as the Tello’s pose estimation is started, type ’track’ to start the hologram tracking

• Now Grab and place the hologram through the Hololens, to give goal positions to the Tello drone

• Type ’land’ to land the drone
