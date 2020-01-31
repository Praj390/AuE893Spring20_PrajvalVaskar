   This script folder contains three python code VIZ circle.py , square_openloop.py ,  square_closedloop.py

As I have already created catkin_ws and assignment_2 package. In that scripts folder is created.
Nodes are made execuable before using it.




1. circle.py
	Task in this code is to move the turtle in circle with constant twist velocity. Twist velocity can be anything but it should be constant throughout the trajectory.
  First initialize the rospy and Publisher is used to give linear and angular velocity to the turtlesim node.

I have used launch file to run the turtlesim and execute the python script circle.py,
	For running the launch file, following command can be used.
   roslaunch assignment_2 turtlesim_circle.launch
   where assignment_2 is package name and turtlesim_circle is launch file name.

2. Square_openloop.py
	Task in this code is to make square from turtlesim of 2 units * 2 units dimensions. To run the turtlesim linear velocity and angular velocity of 0.2 m/s and 0.2 rad/s is given. so in the code same process is followed as per above program.

For running turtlesim and square_openloop.py script under one command, roslaunch is used and for that launch file is created.

To run the launch file, following command is used.
	roslaunch assignment_2 turtlesim_withparams.launch
here the package name is assignment_2 and launch file name is turtlesim_withparams.launch

3. Square_closedloop.py
  	Task in this code is to make square using velocity control of 3*3 units of dimension. For this implementation of PID is done.

Following are the screenshot of the programs



![square5](https://user-images.githubusercontent.com/57248801/73511858-4391ed80-43b5-11ea-80e0-0ef03997be97.png)
![square4](https://user-images.githubusercontent.com/57248801/73511859-4391ed80-43b5-11ea-97e2-0546ff54dd46.png)
![square3](https://user-images.githubusercontent.com/57248801/73511861-4391ed80-43b5-11ea-9a52-e124e723f4e7.png)
![square2](https://user-images.githubusercontent.com/57248801/73511862-4391ed80-43b5-11ea-9ccc-596423b400a5.png)
![square1](https://user-images.githubusercontent.com/57248801/73511863-4391ed80-43b5-11ea-8778-df5fbd7d6757.png)
![circle 3](https://user-images.githubusercontent.com/57248801/73511864-4391ed80-43b5-11ea-8d0c-c5331790ca11.png)
![circle 2](https://user-images.githubusercontent.com/57248801/73511865-442a8400-43b5-11ea-8154-a5413ed27ef9.png)
![circle 1](https://user-images.githubusercontent.com/57248801/73511866-442a8400-43b5-11ea-8205-1b8f3b1d84e4.png)




