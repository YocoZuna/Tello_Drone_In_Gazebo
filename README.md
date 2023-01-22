# Tello_Drone_In_Gazebo

This project was created for the needs of the laboratory on the subject of Identification and Control of Flying Robots. The main goal of the project is to detect the ball by the drone and look next to it. Project is based on ROS2 and Python.

In order to start simulation we have to open new terminal in linux, where script "WiezienLabiryntu.sh" is located and use command "bash WiezienLabiryntu.sh". This command will open all necessary scripts and programs. 

Scripts:
drone.py,
KameraDrona.py
SterowanskoDrone.py,

Have to be lockated in the same directory as WiezienLabiryntu.sh.
In this version of lunch script we have to uncomment "SterowanskiDrone.py". 

KameraDrona is responsible for capture image from drone camera.
SterowanskoDronem is responsible for controlling depend on the values send by KameraDrona.

 
 ## View of drone in Gazebo 
![This is an image](https://github.com/YocoZuna/Tello_Drone_In_Gazebo/blob/main/Gazebo_Start.png)

## Drone camera view
![This is an image](https://github.com/YocoZuna/Tello_Drone_In_Gazebo/blob/main/Obraz_Z_Kamery.png)

## The values send by "Kamera Drona" node

Where p: area of ball contour, x and y: coordinates of ball center, w: area of wall rectangle
![This is an image](https://github.com/YocoZuna/Tello_Drone_In_Gazebo/blob/main/Kamera_Drona_Node.png)




## View of moving drone
![This is an image](https://github.com/YocoZuna/Tello_Drone_In_Gazebo/blob/main/Drone.gif)
