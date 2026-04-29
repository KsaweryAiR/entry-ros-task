# ROS 2  Task — 2-DOF Robot Arm

> **Ubuntu**
> **ROS2 version:** ROS 2 Jazzy
> **Requirements:** Docker + Docker Compose — nothing else needed on your machine

---

### TF_publisher
This node is responsible for bringing the robot to life and setting it in motion.

* **StaticTransformBroadcaster**: Used to handle static transformations. These are published only once to optimize system performance.
* **TransformBroadcaster**: Used for moving joints. Transformation data is continuously published in a loop to the `/tf` topic.
* **Quaternions**: Implemented for orientation representation because they are computationally faster and immune to **Gimbal Lock**, ensuring smooth and reliable rotation math.
* **Time Synchronization**: Uses `header.stamp` with `self.get_clock().now()`. This is primarily implemented to assist with `robot_model` visualization and to allow the system to look up the arm's position from past timestamps.

---

### pose_publisher
This component leverages the built-in power of ROS2 to track the robot's state accurately.

* **Buffer & TransformListener**: To avoid errors during data retrieval, a buffer and listener system is used. The `Buffer` stores the history of transformations, while the `TransformListener` monitors the `/tf` and `/tf_static` topics to automatically populate the buffer with data.
* **lookup_transform Method**: This method is responsible for calculating the real-time position of the robot's end-effector.
* **Visualization (Marker)**: A Marker is rendered in the workspace as it was included in the Rviz configuration during startup, providing a visual reference for the robot's target or current pose.

### verify_robot.py
A standalone script, independent of the ROS2 environment, is responsible for monitoring and validating the simulation’s performance. The script retrieves the /end_effector_pose and maintains a record of the previous state. By calculating the Euclidean distance and applying a sensitivity threshold, it accurately distinguishes intentional robotic arm movement from minor numerical simulation noise.

## Technical Notes & Lessons Learned

### TF Synchronization Challenges
During development, a key focus was placed on **Time Synchronization**. In complex systems (especially those involving RGB-D cameras or 3D mapping), timing issues between `/tf` and sensor data are common. Ensuring accurate `header.stamp` alignment is critical to avoid "extrapolation into the future" errors during spatial data processing.

### Motion Control: ros2_control
For high-precision motion, integrating **ros2_control** is a highly recommended next step. It provides a standardized framework for hardware abstraction, allowing the use of the `JointTrajectoryController` for smooth and deterministic robot arm movements.

### Kinematics and Position Calculation
* **Simple 2DOF Logic**: For low-complexity robots (like a 2DOF arm), end-effector positions can be calculated directly using Forward Kinematics formulas based on data from the `/joint_states` topic.
* **Advanced Planning (MoveIt2)**: For more complex tasks involving obstacle avoidance or high-DOF Inverse Kinematics, **MoveIt2** is the preferred industry-standard tool, which can be seamlessly integrated with this URDF model.
