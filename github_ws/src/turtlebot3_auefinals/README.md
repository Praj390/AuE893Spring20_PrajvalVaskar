# AuE8930: FINAL PROJECT

Submitted on 04/23/2020, by Team 8:

1. Mohammad Anas Imam Khan (C17566828), responsible for Person Tracking logic
2. Prajval Vaskar (C20664702), responsible for Line Following and Stop Sign logic
3. Sagar Virk (C20531221), responsible for Wall Following/Obstacle Avoidance logic
4. Huzefa Shabbir Hussain Kagalwala (C48290423), responsible for integrating all the parts and building it into a single logic
5. Adam Wagner (C10835588), responsible for tuning the PID parameters wherever necessary.

Even though these were the individual contributions, knowledge transfer has ensured that every team member is conversant with all the aspects of the project.


## Initialization
1. **Adding camera to Gazebo TurtleBot3 Burger model:** We used the TurtleBot3 Burger model in Gazebo, which doesn't have a built in camera. So, for adding it in burger, we had to make some changes in  the urdf file which is located in `.../turtlebot3/turtlebot3_description/urdf/`. Clone the camera information in the `turtlebot3_burger.urdf.xacro` and `turtlebot3_burger.gazebo.xacro` files from the respective TurtleBot3 Waffle Pi files.
2. **Building the necessary project packages:** Extracting the given folder in the workspace and building them using the `catkin_make` command.
3. **Adding model directory for sucessful spawning of Gazebo model:** For spawning the model sucessfully, we must update the path of model of built packages. So add path by adding this to your .bashrc file: `export GAZEBO_MODEL_PATH=~path to your model/model`. Point both the `person_sim` and `turtlebot3_auefinals` package here. For launching the world, use the command: `roslaunch turtlebot3_auefinals turtlebot3_autonomy_final.launch`.
4. **Adding required packages:**

	a. `darknet_ros` package:  `darknet_ros` package is used for detecting the stop sign. The package was built using instructions given [here](https://github.com/leggedrobotics/darknet_ros)

	b. Packages required for leg detection: For leg detection, `People_Detection` folder was provided under which `detector_msg_to_pose_array`,`leg_detector` and `tc_people_tracker` packages were 	    built by `catkin_make` command from the terminal.

**NOTE:** Other packages like `wu_ros_tools_kinetic` were also built for the Camera Detection part in order to resolve dependency errors while building the `darknet_ros` package.


## Task 1: Wall following/Obstacle avoidance:
In this part, the Turtlebot had to successfully follow the wall and avoid the obstacles until it reached the yellow line. We also had to create a map of this corridor using a SLAM package of our choice.
To achieve the objective, the following approach was used:
1. The FOV of the robot was divided into 2 sectors:
	- Front right sector, having a sector angle of 40 degrees [300:339].
	- Front left sector, having a sector angle of 60 degrees[20:80].
2. Direct PID implementation was very difficult, so it was decided to implement digitized PID control
3. The control parameters were set as such that the bot follows the walls, keeping equal distance from them.
4. The PID control was only implemented to govern the steering of the bot and linear velocities were kept constant.

## Task 2: Line following:
Here, the Turtlebot had to successfully follow the yellow line. While following line it had to detect the stop sign and stop for 3 seconds.
To achieve the objective, the following approach was used:
1. The CV Bridge and vision_opencv packages were copied in the `src` folder of our workspaces as provided which was already done in previous assignments.
2. We implemented a controller to follow the centroid formed on the line of whichever color we want it to track.
3. The image crop was also tuned so that the robots field of view is sufficient for the tracking to take place.
4. For stopping the TurtleBot3, darknet_ros will detect the sign and a counter will be activated which will allow the TurtleBot3 to stop near the stop sign for 3 seconds. Through this delay counter we can change the location where we want to stop the TurtleBot3.

## Task 3: Human tracking:
In the final part, the Turtlebot3 had to use a trained DL network to identify the human in the environment and follow it around (using leg detector packages). The human in Gazebo could be teleoperated around using the keyboard which was already a part of the given Gazebo environment. The following steps were taken to achieve this:
1. Using the `leg_detector` package, the position of the person is found. This is done by recognizing the 'U' shape created by the laser scan, when it scans the legs of the person.
2. The position of the robot in the global frame is found using the `nav_msgs/Odometry` package. The roll, pitch and yaw are also found by converting the quaternion notation to Euler notation.
3. The difference in the position and the orientation between the person and robot is used to feed the error to the digital PID control given to the steering and linear velocity to track the person.


## Final Integration:
1. The `integrated.py` script is written such a way that it automatically switches task depending upon the location of the bot. For example, after wall following and obstcale avoidance, turtlebot3 will detect the yellow line the code will switch to follow line. While following the yellow line `darknet_ros` package will detect the stop sign and it will trigger the code which will stop the TurtleBot3 for 3 seconds near the stop sign. Finally after finishing to follow yellow line, script will be switched into person following code which uses leg detector package and turtlebot3 will follow the human which can be teleop by keyboard using X-Terminal which is launched after spwaning the model. We have created launch file such that it will launch all the nodes and topics that are to be used for all the above tasks.
2. The code is based on the logic that the Bot will follow the line only when a centroid is formed, which is only formed when a line comes into the Bot's FOV. Thus, when no centroid is formed and the flag for stop sign detection hasn't been raised, the Bot will execute the wall following and obstacle avoidance logic. When the line comes into view and a centroid is formed, the Bot tracks the centroid, hence, performing line following. When the stop sign is detected, based on the counter delay, the Bot stops for 3 seconds near the Stop sign. Now the stop sign flag is raised. When no centroid is formed and the flag is True for stop sign being found, the Bot will track the person in the environment.

To launch the file, use this command in the terminal `roslaunch turtlebot3_auefinals turtlebot3_autonomy_final.launch`



