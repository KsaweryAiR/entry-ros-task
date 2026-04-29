#!/usr/bin/env python3
"""
TF Publisher Node
-----------------
Publishes the TF2 transform chain for a 2-DOF robot arm.

Chain layout:
    world
      └── base_link       (static, identity)
            └── link1     (dynamic, rotates around Z over time)
                  └── link2  (static offset: x=0.3m from link1)
                        └── end_effector  (static offset: x=0.2m from link2)

Your task (TODO 1):
    Implement the _broadcast() method so that:
    - 'world' → 'base_link'       is a static identity transform
    - 'base_link' → 'link1'       rotates around Z with amplitude 45° (0.785 rad)
                                  at a frequency of 0.5 Hz
    - 'link1' → 'link2'           is a static transform with x=0.3m offset
    - 'link2' → 'end_effector'    is a static transform with x=0.2m offset

    Use StaticTransformBroadcaster for transforms that never change.
    Use TransformBroadcaster for transforms that change over time.
"""
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from tf2_ros import TransformException
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener
from visualization_msgs.msg import Marker

class TFPublisher(Node):

    def __init__(self):
        super().__init__('tf_publisher')
        self.get_logger().info('TFPublisher started.')

        self.x_ = None
        self.y_ = None
        self.z_ = None
        self.w_ = None

        self.tf_buffer_ = Buffer()
        self.tf_listener_ = TransformListener(self.tf_buffer_, self)
        
        self.publisher_ = self.create_publisher(PoseStamped, '/end_effector_pose', 10)
        self.marker_pub = self.create_publisher(Marker, '/end_effector_marker', 10)
        self.timer_ = self.create_timer(0.1, self.timer_callback)

    def timer_callback(self):
        try:
            t = self.tf_buffer_.lookup_transform(
                'world',
                'end_effector',
                rclpy.time.Time())

            msg = PoseStamped()
            msg.header.stamp = t.header.stamp
            msg.header.frame_id = 'world'
            
            msg.pose.position.x = t.transform.translation.x
            msg.pose.position.y = t.transform.translation.y
            msg.pose.position.z = t.transform.translation.z
            
            msg.pose.orientation.x = t.transform.rotation.x
            msg.pose.orientation.y = t.transform.rotation.y
            msg.pose.orientation.z = t.transform.rotation.z
            msg.pose.orientation.w = t.transform.rotation.w

            self.publisher_.publish(msg)

            self.x_ = msg.pose.position.x
            self.y_ = msg.pose.position.y
            self.z_ = msg.pose.orientation.z
            self.w_ = msg.pose.orientation.w

            self.TF_publisher()
            self.marker(msg)

            
        except TransformException as ex:
            self.get_logger().warn(f'Could not transform world to end_effector: {ex}')

        

    def TF_publisher(self):
        try: 
            self.get_logger().info(f"""                   
                TF:
                Translation:
                x: {self.x_:.2f}
                y: {self.y_:.2f}
                Rotation:
                z: {self.z_:.2f}
                w: {self.w_:.2f}
                """)
            
        except Exception as e:
            self.get_logger().warn(str(e))

    def marker(self, pose_msg):
        marker = Marker()
        marker.header = pose_msg.header
        marker.ns = 'end_effector'
        marker.id = 0
        marker.type = Marker.SPHERE
        marker.action = Marker.ADD
        marker.pose = pose_msg.pose
        marker.scale.x = 0.1
        marker.scale.y = 0.1
        marker.scale.z = 0.1
        marker.color.a = 1.0
        marker.color.r = 1.0
        marker.color.g = 0.0
        marker.color.b = 0.0
        
        self.marker_pub.publish(marker)


def main(args=None):
    rclpy.init(args=args)
    node = TFPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

